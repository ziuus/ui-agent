# Examples of UI Agent usage

Try these commands to see ui-agent in action:

## 1. Basic Click
```bash
ui-agent click "Google search box"
```

## 2. Click with Custom Delay
```bash
ui-agent click "Login button" --delay 3.0
```

## 3. Type Text
```bash
ui-agent type "hello@example.com"
```

## 4. Type with Character Interval
```bash
ui-agent type "MyPassword123" --interval 0.1
```

## 5. Login Flow Example
```bash
# Click email field
ui-agent click "Email input field"

# Type email
ui-agent type "user@example.com" --interval 0.05

# Click password field
ui-agent click "Password input field"

# Type password
ui-agent type "SecurePass123" --interval 0.1

# Click login button
ui-agent click "Login button"
```

## 6. Form Filling Example
```bash
ui-agent click "First Name field"
ui-agent type "John" --interval 0.05

ui-agent click "Last Name field"
ui-agent type "Doe" --interval 0.05

ui-agent click "Email field"
ui-agent type "john.doe@example.com" --interval 0.03

ui-agent click "Submit button"
```

## 7. Take a Screenshot
```bash
ui-agent screenshot
# or save to file
ui-agent screenshot --output current_screen.png
```

## 8. Verbose Mode
```bash
ui-agent click "Element description" --verbose
ui-agent type "text" -v
```

## Tips:
- Use descriptive element names: "red submit button" instead of just "button"
- Move mouse to top-left corner anytime to abort an action
- Use `--delay` to give yourself time to inspect before clicking
- Use `--interval` for slower typing on systems that might miss keystrokes
- Check `ui-agent --help` for all available options
