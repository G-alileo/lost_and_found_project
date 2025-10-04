# Utility Classes Reference Guide

This guide shows how to replace the custom CSS classes that used `@apply` with Tailwind utility classes directly in your HTML.

## Button Classes

### Instead of `btn-primary` class:
```html
<!-- Old way (with @apply) -->
<button class="btn-primary">Click me</button>

<!-- New way (direct utilities) -->
<button class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200">Click me</button>
```

### Instead of `btn-secondary` class:
```html
<!-- Old way -->
<button class="btn-secondary">Click me</button>

<!-- New way -->
<button class="px-6 py-3 border-2 border-blue-600 text-blue-600 hover:bg-blue-600 hover:text-white font-medium rounded-lg transition-all duration-200">Click me</button>
```

## Card Classes

### Instead of `card` class:
```html
<!-- Old way -->
<div class="card">Content</div>

<!-- New way -->
<div class="rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 card">Content</div>
```

## Form Classes

### Instead of `input-field` class:
```html
<!-- Old way -->
<input class="input-field" type="text">

<!-- New way -->
<input class="px-4 py-3 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 input-field" type="text">
```

### Instead of `nav-link` class:
```html
<!-- Old way -->
<a class="nav-link">Link</a>

<!-- New way -->
<a class="hover:text-blue-600 transition-colors duration-200 font-medium nav-link">Link</a>
```

## Badge Classes

### Instead of badge classes:
```html
<!-- badge-lost -->
<span class="bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 px-3 py-1 rounded-full text-sm font-medium">Lost</span>

<!-- badge-found -->
<span class="bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 px-3 py-1 rounded-full text-sm font-medium">Found</span>

<!-- badge-matched -->
<span class="bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300 px-3 py-1 rounded-full text-sm font-medium">Matched</span>
```

## Layout Classes

### Instead of `items-grid` class:
```html
<!-- Old way -->
<div class="items-grid">Items</div>

<!-- New way -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">Items</div>
```

### Instead of `notification-popup` class:
```html
<!-- Old way -->
<div class="notification-popup">Notification</div>

<!-- New way -->
<div class="fixed top-4 right-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-4 z-50 max-w-sm notification-popup">Notification</div>
```

## Table Classes

### Instead of table classes:
```html
<!-- data-table -->
<table class="w-full border-collapse">

<!-- data-table th -->
<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider border-b border-gray-200 dark:border-gray-700">

<!-- data-table td -->
<td class="px-6 py-4 whitespace-nowrap border-b border-gray-200 dark:border-gray-700">
```

## Form Classes

### Instead of form classes:
```html
<!-- form-group -->
<div class="mb-6">

<!-- form-label -->
<label class="block text-sm font-medium mb-2 form-label">

<!-- form-error -->
<div class="text-red-500 text-sm mt-1">

<!-- filter-section -->
<div class="p-6 rounded-xl mb-8 filter-section">

<!-- stats-card -->
<div class="p-6 rounded-xl text-center stats-card">

<!-- stats-number -->
<div class="text-3xl font-bold text-blue-600 mb-2">

<!-- stats-label -->
<div class="text-sm font-medium stats-label">

<!-- spinner -->
<div class="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin">
```

## Usage Instructions

1. Replace the CSS file reference in your HTML files:
   ```html
   <!-- Change this -->
   <link rel="stylesheet" href="../css/tailwind.css">
   
   <!-- To this -->
   <link rel="stylesheet" href="../css/custom-styles.css">
   ```

2. Update your HTML elements to use the utility classes directly instead of the custom classes.

3. Keep the custom CSS variables and animations from `custom-styles.css` for theme consistency.
