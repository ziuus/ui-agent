"""Vision API integration using Google Gemini with model fallback."""

import json
import re
from typing import List, Tuple
import google.generativeai as genai
from rich.console import Console


class VisionAnalyzer:
    """Analyzes screenshots using Gemini vision API."""

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        """Initialize vision analyzer with API key.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.console = Console()
        self.model_name = self._select_model_name(model_name)
        self.model = genai.GenerativeModel(self.model_name)

    def _select_model_name(self, preferred: str) -> str:
        """Pick a working model name from preferred value or API-discovered models."""
        fallback_candidates = [
            preferred,
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash",
            "gemini-1.5-pro-latest",
            "gemini-1.5-pro",
        ]

        available = self._available_generate_content_models()
        if available:
            priority = [self._normalize_model_name(name) for name in fallback_candidates if name]
            for candidate in priority:
                if candidate in available:
                    return candidate

            # Prefer flash variants first for latency/cost.
            for candidate in available:
                if "flash" in candidate:
                    return candidate

            return available[0]

        # If model listing is unavailable, try preferred directly.
        return self._normalize_model_name(preferred)

    def _available_generate_content_models(self) -> List[str]:
        """Return model IDs that support generateContent."""
        try:
            models = []
            for model in genai.list_models():
                methods = getattr(model, "supported_generation_methods", []) or []
                if "generateContent" not in methods:
                    continue
                normalized = self._normalize_model_name(getattr(model, "name", ""))
                if normalized and normalized.startswith("gemini"):
                    models.append(normalized)
            # Stable ordering without duplicates.
            return list(dict.fromkeys(models))
        except Exception:
            return []

    def _normalize_model_name(self, name: str) -> str:
        """Convert model IDs like models/gemini-2.0-flash to gemini-2.0-flash."""
        value = (name or "").strip()
        if value.startswith("models/"):
            return value.split("/", 1)[1]
        return value

    def locate_element(self, screenshot_bytes: bytes, description: str) -> Tuple[int, int, int, int]:
        """Locate UI element in screenshot and return bounding box.
        
        Args:
            screenshot_bytes: Screenshot as bytes (PNG format)
            description: Text description of element to find
            
        Returns:
            Tuple of (ymin, xmin, ymax, xmax) normalized to 0-1000 scale
            
        Raises:
            ValueError: If element not found or API returns invalid response
        """
        prompt = f"""Locate the UI element described as: "{description}"

Return ONLY a JSON object with this exact format (no markdown, no explanation):
{{
    "found": true,
    "ymin": <integer 0-1000>,
    "xmin": <integer 0-1000>,
    "ymax": <integer 0-1000>,
    "xmax": <integer 0-1000>,
    "confidence": <float 0-1>,
    "element_type": "<what you found>"
}}

If you cannot find the element, return:
{{
    "found": false,
    "reason": "<explanation>"
}}

IMPORTANT: Normalize coordinates to 0-1000 scale where:
- Top-left corner = (0, 0)
- Bottom-right corner = (1000, 1000)
- ymin/ymax are vertical (top to bottom)
- xmin/xmax are horizontal (left to right)"""

        # Show spinner while waiting for API
        with self.console.status("[bold green]Analyzing screenshot...", spinner="dots"):
            try:
                # Convert bytes to Image
                from PIL import Image
                import io
                image = Image.open(io.BytesIO(screenshot_bytes))
                
                response = self.model.generate_content([prompt, image])
                maybe_raise = getattr(response, "raise_for_exception", None)
                if callable(maybe_raise):
                    maybe_raise()
                
                # Parse response
                response_text = response.text.strip()
                
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if not json_match:
                    raise ValueError(f"Invalid API response format: {response_text}")
                
                result = json.loads(json_match.group())
                
                if not result.get("found", False):
                    reason = result.get("reason", "Element not found")
                    raise ValueError(f"Element not found: {reason}")
                
                # Extract and validate coordinates
                required_fields = ["ymin", "xmin", "ymax", "xmax"]
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing field in API response: {field}")
                
                ymin = int(result["ymin"])
                xmin = int(result["xmin"])
                ymax = int(result["ymax"])
                xmax = int(result["xmax"])
                
                # Validate ranges
                if not (0 <= ymin <= 1000 and 0 <= xmin <= 1000 and
                        0 <= ymax <= 1000 and 0 <= xmax <= 1000):
                    raise ValueError(
                        f"Coordinates out of range (0-1000): "
                        f"ymin={ymin}, xmin={xmin}, ymax={ymax}, xmax={xmax}"
                    )
                
                if ymin > ymax or xmin > xmax:
                    raise ValueError(
                        f"Invalid bounding box: min > max. "
                        f"ymin={ymin}, ymax={ymax}, xmin={xmin}, xmax={xmax}"
                    )
                
                return (ymin, xmin, ymax, xmax)
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse API response as JSON: {response_text}") from e
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower():
                    raise ValueError(
                        "API rate limit exceeded. Please wait a moment and try again."
                    ) from e
                if "401" in str(e) or "invalid" in str(e).lower():
                    raise ValueError(
                        "Invalid or expired API key. Check GEMINI_API_KEY configuration."
                    ) from e
                raise

    def verify_element(
        self, screenshot_bytes: bytes, description: str, confidence_threshold: float = 0.7
    ) -> bool:
        """Verify that an element exists in the current screenshot.
        
        Args:
            screenshot_bytes: Screenshot as bytes
            description: Element description
            confidence_threshold: Minimum confidence (0-1)
            
        Returns:
            True if element found with sufficient confidence
        """
        try:
            # This would need a modified prompt to return confidence
            # For now, we just try to locate it
            self.locate_element(screenshot_bytes, description)
            return True
        except ValueError:
            return False
