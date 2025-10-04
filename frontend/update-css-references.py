#!/usr/bin/env python3
"""
Script to update CSS references in all HTML files from tailwind.css to custom-styles.css
"""

import os
import glob

def update_html_files():
    # Get all HTML files in the pages directory
    html_files = glob.glob("pages/*.html")
    
    updated_files = []
    
    for file_path in html_files:
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace the CSS reference
            old_reference = '../css/tailwind.css'
            new_reference = '../css/custom-styles.css'
            
            if old_reference in content:
                updated_content = content.replace(old_reference, new_reference)
                
                # Write the updated content back
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                
                updated_files.append(file_path)
                print(f"✅ Updated: {file_path}")
            else:
                print(f"ℹ️  No update needed: {file_path}")
                
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n🎉 Successfully updated {len(updated_files)} files!")
    return updated_files

if __name__ == "__main__":
    print("🔄 Updating CSS references in HTML files...")
    update_html_files()
