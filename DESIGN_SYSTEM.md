# 🎨 Design System & Style Guide

## Color Palette

### Primary Colors
```
Indigo Primary:    #667eea
                   ████████████████████ RGB(102, 126, 234)
                   
Purple Secondary:  #764ba2
                   ████████████████████ RGB(118, 75, 162)
```

### Status Colors
```
Success (Green):   #51cf66
                   ████████████████████ RGB(81, 207, 102)
                   
Danger (Red):      #ff6b6b
                   ████████████████████ RGB(255, 107, 107)
                   
Warning (Orange):  #ffa94d
                   ████████████████████ RGB(255, 169, 77)
                   
Info (Blue):       #4dabf7
                   ████████████████████ RGB(77, 171, 247)
```

### Neutral Colors
```
Background Light:  #f8f9fa
                   ████████████████████ RGB(248, 249, 250)
                   
Background White:  #ffffff
                   ████████████████████ RGB(255, 255, 255)
                   
Text Dark:         #2c3e50
                   ████████████████████ RGB(44, 62, 80)
                   
Text Gray:         #6c757d
                   ████████████████████ RGB(108, 117, 125)
                   
Border Light:      #dee2e6
                   ████████████████████ RGB(222, 226, 230)
```

---

## Typography

### Font Family
**Poppins** (Google Fonts)
- Modern and clean
- Excellent readability
- Professional appearance
- Web-optimized

### Font Weights & Sizes

#### Headings
```
H1 - 3.5em (56px), Weight: 800 (Extra Bold)
    Email & SMS Spam Detector

H2 - 2em (32px), Weight: 700 (Bold)
    Single Message Analysis

H3 - 1.5em (24px), Weight: 700 (Bold)
    How It Works

H4 - 1.2em (19px), Weight: 600 (Semi-Bold)
    Confidence Score
```

#### Body Text
```
Paragraph - 1em (16px), Weight: 400 (Regular)
    This is a regular paragraph with normal weight.

Small - 0.95em (15px), Weight: 500 (Medium)
    This is smaller text with medium weight.

Caption - 0.85em (13px), Weight: 500 (Medium)
    This is caption text.

Label - 1em (16px), Weight: 600 (Semi-Bold)
    Form Label
```

---

## Spacing System

### Base Unit: 8px

```
xs:  4px   (0.5 unit)
sm:  8px   (1 unit)    ▮
md: 16px   (2 units)   ▮▮
lg: 24px   (3 units)   ▮▮▮
xl: 32px   (4 units)   ▮▮▮▮
2xl:40px   (5 units)   ▮▮▮▮▮
3xl:48px   (6 units)   ▮▮▮▮▮▮
```

### Common Spacing
- **Padding**: 16px, 24px, 32px
- **Margin**: 12px, 20px, 30px
- **Gap**: 12px, 20px, 30px

---

## Shadow System

### Shadow Hierarchy

```
Shadow Small (--shadow-sm)
  0 2px 8px rgba(0,0,0,0.08)
  └─ Subtle, for small elements

Shadow Medium (--shadow-md)
  0 8px 24px rgba(0,0,0,0.12)
  └─ Standard, for cards and buttons

Shadow Large (--shadow-lg)
  0 16px 40px rgba(0,0,0,0.15)
  └─ Prominent, for modals and overlays
```

### Usage
- **Cards**: shadow-md
- **Buttons**: shadow-md (hover: shadow-lg)
- **Navigation**: shadow-md
- **Hover States**: shadow-lg
- **Active Elements**: shadow-sm (inset)

---

## Border Radius

### Sizes
```
Small:    6px   ▮
Medium:   10px  ▮
Large:    12px  ▮
Extra:    14px  ▮
Full:     50%   ●
```

### Usage
- **Buttons**: 10px
- **Cards**: 14-16px
- **Inputs**: 10px
- **Small Elements**: 6px
- **Badges**: 20px (pill-shaped)

---

## Animations

### Timing Functions
```
ease-out:           Smooth entrance
ease-in:            Smooth exit
cubic-bezier:       Custom curves
linear:             Constant speed
```

### Common Animations

#### Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
Duration: 0.5s
```

#### Slide Down
```css
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
Duration: 0.6s
```

#### Slide Up
```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
Duration: 0.6s
```

#### Spin (Loading)
```css
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
Duration: 1s, Linear
```

### Interaction Animations
- **Hover**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Click**: 0.2s ease
- **Loading**: 1s linear (infinite)
- **Entrance**: 0.5s ease-out

---

## Button Styles

### Primary Button
```
Background: Linear gradient (Primary → Secondary)
Color: White
Padding: 14px 32px
Border Radius: 10px
Font Weight: 600
Shadow: shadow-md
Hover: translateY(-3px), shadow-lg
Active: translateY(-1px)
```

### Secondary Button
```
Background: Light gray (#f8f9fa)
Color: Dark text (#2c3e50)
Padding: 14px 32px
Border Radius: 10px
Font Weight: 600
Shadow: shadow-sm
Hover: darker background
```

### Success Button
```
Background: Linear gradient (Green)
Color: White
Same as Primary Button
```

---

## Input Styles

### Text Input / Textarea
```
Background: Light gray (#f8f9fa)
Border: 2px solid (#dee2e6)
Padding: 14px
Border Radius: 10px
Font: Poppins, 1em

Focus:
  Border Color: Primary (#667eea)
  Background: White
  Box Shadow: 0 0 0 4px rgba(102, 126, 234, 0.1)
```

---

## Card Styles

### Standard Card
```
Background: White
Border Radius: 16px
Padding: 40px
Shadow: shadow-lg
Border: 1px solid rgba(255, 255, 255, 0.5)
```

### Stat Card
```
Background: White
Padding: 30px
Border Radius: 14px
Shadow: shadow-md
Border Top: 4px solid (Primary)

Hover:
  Transform: translateY(-8px)
  Shadow: shadow-lg
```

### Example Card
```
Background: White
Padding: 25px
Border Radius: 14px
Border: 2px solid (#dee2e6)
Shadow: shadow-sm

Hover:
  Border Color: Primary
  Transform: translateY(-8px)
  Shadow: shadow-lg
  Shimmer Effect
```

---

## Result Card Styles

### Spam Result
```
Background: Linear gradient (Red with transparency)
Border Left: 6px solid Red (#ff6b6b)
Padding: 30px
Border Radius: 14px
Title Color: Red
```

### Legitimate Result
```
Background: Linear gradient (Green with transparency)
Border Left: 6px solid Green (#51cf66)
Padding: 30px
Border Radius: 14px
Title Color: Green
```

---

## Badge Styles

### Spam Badge
```
Background: Rgba(255, 107, 107, 0.2)
Color: Red (#ff6b6b)
Border: 1px solid Red
Padding: 8px 14px
Border Radius: 20px
Font Weight: 600
Text Transform: Uppercase
```

### Legitimate Badge
```
Background: Rgba(81, 207, 102, 0.2)
Color: Green (#51cf66)
Border: 1px solid Green
Same as Spam Badge
```

---

## Progress Bar

```
Container:
  Height: 24px
  Background: Light gray
  Border Radius: 12px
  Border: 2px solid border-light
  
Fill:
  Background: Linear gradient (Primary → Secondary)
  Height: 100%
  Transition: 0.6s cubic-bezier(0.4, 0, 0.2, 1)
  Display: Percentage text on bar
```

---

## Table Styles

### Header Row
```
Background: Linear gradient (Primary → Secondary)
Color: White
Padding: 16px
Font Weight: 600
Text Transform: Uppercase
Letter Spacing: 0.5px
Font Size: 0.85em
```

### Body Rows
```
Padding: 14px 16px
Border Bottom: 1px solid (#dee2e6)

Hover:
  Background: Light gray
  Shadow: Inset, 0 0 10px rgba(102, 126, 234, 0.08)
```

---

## Responsive Breakpoints

```
Mobile First:
  Default: < 768px (Mobile)
  Tablet: 768px - 1199px
  Desktop: 1200px+

Changes at 768px:
  • Single column layouts
  • Adjusted font sizes
  • Full-width buttons
  • Touch-friendly sizing
```

---

## CSS Variables Reference

```css
:root {
  /* Colors */
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #51cf66;
  --danger: #ff6b6b;
  --warning: #ffa94d;
  --info: #4dabf7;
  --bg-light: #f8f9fa;
  --bg-white: #ffffff;
  --text-dark: #2c3e50;
  --text-gray: #6c757d;
  --border-light: #dee2e6;
  
  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.12);
  --shadow-lg: 0 16px 40px rgba(0,0,0,0.15);
}
```

---

## Accessibility Features

✅ **Color Contrast**
- Text on backgrounds has minimum 4.5:1 ratio
- Status colors have distinct meanings
- Not reliant on color alone

✅ **Typography**
- Large, readable font (16px minimum)
- Good line height (1.6)
- Clear hierarchy

✅ **Spacing**
- Touch targets: 44px minimum
- Clear visual groups
- Adequate white space

✅ **Interactive Elements**
- Clear focus states
- Visible hover effects
- Descriptive labels

---

## Usage Examples

### Creating a New Card
```html
<div class="card">
  <h2>Card Title</h2>
  <p class="card-subtitle">Subtitle text</p>
  <!-- Content -->
</div>
```

### Creating a Button
```html
<button>Primary Button</button>
<button class="btn-secondary">Secondary Button</button>
<button class="btn-success">Success Button</button>
```

### Creating a Result
```html
<div class="result-container result-spam">
  <div class="result-title">🚨 SPAM DETECTED!</div>
  <!-- Result content -->
</div>
```

---

## Customization Guide

### Changing Primary Color
1. Update all instances of `#667eea` in CSS
2. Update gradient backgrounds
3. Update CSS variables
4. Test on all components

### Changing Font
1. Replace Google Fonts import
2. Update font-family in CSS
3. Adjust font weights if needed
4. Test readability

### Adjusting Spacing
1. Modify base unit (currently 8px)
2. Update all spacing values proportionally
3. Retest layout on all breakpoints

---

## Best Practices

✅ **DO:**
- Use CSS variables for colors
- Follow the spacing system
- Use consistent shadows
- Test on mobile devices
- Use the defined palette

❌ **DON'T:**
- Mix color schemes
- Use hardcoded colors
- Ignore responsive breakpoints
- Create inconsistent spacing
- Over-animate interactions

---

**Design System Version**: 1.0
**Last Updated**: April 20, 2026
**Status**: ✅ Complete and Ready to Use
