# Testing Guide

## Quick Start Testing

The local server is running at: **http://localhost:8000**

Open this URL in your browser to view the website.

## Testing Checklist

### ✅ Desktop Testing (> 1024px)

- [ ] Navigation bar displays correctly with all menu items
- [ ] Logo is visible and styled
- [ ] "Learn" dropdown works on hover
- [ ] Hero section displays with gradient background
- [ ] All 6 test site cards are visible
- [ ] Cards alternate between left/right image placement
- [ ] Footer displays in 4-column layout
- [ ] Social media icons are visible
- [ ] All links are styled correctly
- [ ] Hover effects work on cards and links

### ✅ Tablet Testing (768px - 1024px)

- [ ] Layout adjusts to tablet width
- [ ] Navigation remains horizontal
- [ ] Cards maintain alternating layout
- [ ] Footer switches to 2-column layout
- [ ] Images scale appropriately

### ✅ Mobile Testing (< 768px)

- [ ] Hamburger menu icon appears
- [ ] Clicking hamburger opens side menu
- [ ] Side menu slides in from right
- [ ] Navigation items stack vertically
- [ ] "Learn" dropdown expands on click
- [ ] Cards stack vertically (image on top)
- [ ] Footer switches to single column
- [ ] All text remains readable
- [ ] Touch targets are adequate (min 44px)

### ✅ Functionality Testing

- [ ] Mobile menu opens/closes smoothly
- [ ] Clicking outside menu closes it
- [ ] ESC key closes mobile menu
- [ ] Dropdown menu works on both hover and click
- [ ] Smooth scrolling works (if anchor links present)
- [ ] No console errors
- [ ] JavaScript loads correctly

### ✅ Accessibility Testing

- [ ] Tab navigation works through all elements
- [ ] Focus indicators are visible
- [ ] ARIA labels are present
- [ ] Heading hierarchy is correct (h1 → h2 → h3)
- [ ] Images have alt text
- [ ] Color contrast is sufficient
- [ ] Screen reader can navigate the page

### ✅ Performance Testing

- [ ] Page loads in < 2 seconds
- [ ] No layout shift on load
- [ ] Images load properly
- [ ] CSS and JS files load without errors
- [ ] No 404 errors in console

### ✅ Cross-Browser Testing

Test in multiple browsers:
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## Known Issues to Check

1. **Missing Images**: Placeholder images need to be generated
   - Open `images/generate-placeholders.html`
   - Download all images
   - Verify they display correctly

2. **Font Loading**: Google Fonts require internet connection
   - Check if fonts load properly
   - Verify fallback fonts work offline

3. **Icon Loading**: Font Awesome requires internet
   - Check if icons display
   - Consider downloading Font Awesome for offline use

## Testing Tools

### Browser DevTools
- **Responsive Design Mode**: Test different screen sizes
- **Console**: Check for JavaScript errors
- **Network Tab**: Monitor resource loading
- **Lighthouse**: Run performance audit

### Accessibility Tools
- **WAVE**: Web accessibility evaluation tool
- **axe DevTools**: Accessibility testing extension
- **Screen Reader**: Test with NVDA (Windows) or VoiceOver (Mac)

### Performance Tools
- **Lighthouse**: Built into Chrome DevTools
- **PageSpeed Insights**: Google's performance tool
- **WebPageTest**: Detailed performance analysis

## Manual Testing Steps

### 1. Desktop Navigation
```
1. Open http://localhost:8000
2. Hover over "Learn" menu item
3. Verify dropdown appears
4. Click each navigation link
5. Verify hover effects work
```

### 2. Mobile Menu
```
1. Resize browser to < 768px width
2. Click hamburger menu icon
3. Verify menu slides in from right
4. Click "Learn" to expand dropdown
5. Click outside menu to close
6. Press ESC key to close
```

### 3. Card Interactions
```
1. Hover over each card image
2. Verify lift effect and shadow
3. Click card titles
4. Verify link styling
```

### 4. Footer Links
```
1. Scroll to footer
2. Hover over each link
3. Verify hover effects
4. Click social media icons
```

## Automated Testing (Optional)

If you want to add automated tests, consider:

### Jest for JavaScript
```javascript
// Example test
test('Mobile menu toggles correctly', () => {
  const toggler = document.getElementById('navbarToggler');
  const menu = document.getElementById('navbarMenu');
  
  toggler.click();
  expect(menu.classList.contains('active')).toBe(true);
  
  toggler.click();
  expect(menu.classList.contains('active')).toBe(false);
});
```

### Cypress for E2E Testing
```javascript
// Example E2E test
describe('Navigation', () => {
  it('should open mobile menu', () => {
    cy.visit('http://localhost:8000');
    cy.viewport('iphone-6');
    cy.get('#navbarToggler').click();
    cy.get('#navbarMenu').should('have.class', 'active');
  });
});
```

## Bug Reporting Template

If you find issues, document them:

```markdown
### Bug: [Brief Description]

**Severity**: Critical / High / Medium / Low

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Environment**:
- Browser: Chrome 120
- OS: Windows 11
- Screen Size: 1920x1080

**Screenshots**:
[Attach screenshots if applicable]
```

## Performance Benchmarks

Target metrics:
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1
- **Total Page Size**: < 500KB

## Accessibility Benchmarks

Target scores:
- **WAVE**: 0 errors
- **Lighthouse Accessibility**: > 95
- **Color Contrast**: AAA rating
- **Keyboard Navigation**: 100% functional

## Next Steps After Testing

1. ✅ Fix any bugs found
2. ✅ Optimize performance issues
3. ✅ Improve accessibility scores
4. ✅ Add missing features
5. ✅ Document changes
6. ✅ Deploy to production (if applicable)

---

**Happy Testing! 🧪**