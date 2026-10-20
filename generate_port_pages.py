#!/usr/bin/env python3
"""
Port Pages Generator Script
Generates all 49 port pages from Excel data with consistent UI
"""

import pandas as pd
import re
from pathlib import Path

# Configuration
EXCEL_PATH = r"D:\FalconXoft Ship Chandler\Website Data\Ship_Chandler_SEO_49_Pages_FULL.xlsx"
OUTPUT_DIR = Path(r"D:\FalconXoft Ship Chandler\Nigeria\ports")
SHEET_NAME = "SEO Pages"

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_port_name_for_cta(page_name):
    """Extract port name for CTA (e.g., 'Bissau Port', 'Dar Es Salaam Port')"""
    # Remove common prefixes/suffixes
    name = page_name.replace('Ship Chandler', '').strip()
    name = name.replace('ship chandler', '').strip()
    
    # Handle special cases
    if '-' in name:
        # "Bissau Ship Chandler - Guinea" -> "Bissau"
        name = name.split('-')[0].strip()
    
    # If it doesn't end with 'Port', add it
    if not name.lower().endswith('port'):
        return f"{name} Port"
    
    return name

def format_content_html(content):
    """Convert markdown-like content to HTML with proper structure"""
    if pd.isna(content):
        return ""
    
    content = str(content)
    html_parts = []
    
    # Split by markdown headers (##)
    sections = re.split(r'\n## ', content)
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        lines = section.split('\n')
        
        if i == 0:
            # First section (before any ## header)
            # Just paragraphs
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Check if line has **text** pattern (bold markdown)
                    if line.startswith('**') and line.endswith('**'):
                        # Remove ** and wrap in strong
                        bold_text = line[2:-2]
                        html_parts.append(f"            <p><strong>{bold_text}</strong></p>")
                    else:
                        html_parts.append(f"            <p>{line}</p>")
        else:
            # Sections with headers
            # First line is the header
            header = lines[0].strip()
            html_parts.append(f"\n            <h2>{header}</h2>")
            
            current_list = []
            in_list = False
            
            for line in lines[1:]:
                line = line.strip()
                
                if not line:
                    continue
                
                # Check if it's a list item
                if line.startswith('- '):
                    in_list = True
                    list_item = line[2:].strip()
                    current_list.append(f"              <li>{list_item}</li>")
                else:
                    # If we were in a list, close it
                    if in_list and current_list:
                        html_parts.append("            <ul>")
                        html_parts.extend(current_list)
                        html_parts.append("            </ul>")
                        current_list = []
                        in_list = False
                    
                    # Check if line has **text** pattern (bold markdown)
                    if line.startswith('**') and line.endswith('**'):
                        # Remove ** and wrap in strong
                        bold_text = line[2:-2]
                        html_parts.append(f"            <p><strong>{bold_text}</strong></p>")
                    else:
                        # Add as paragraph
                        html_parts.append(f"            <p>{line}</p>")
            
            # Close any remaining list
            if in_list and current_list:
                html_parts.append("            <ul>")
                html_parts.extend(current_list)
                html_parts.append("            </ul>")
    
    return '\n'.join(html_parts)

def generate_page_html(row):
    """Generate complete HTML page for a port"""
    page_name = str(row['Page Name'])
    h1 = str(row['H1'])
    meta_title = str(row['Meta Title'])
    meta_description = str(row['Meta Description'])
    full_content = str(row['Full SEO Description'])
    
    # Generate filename
    filename = slugify(page_name) + '.html'
    
    # Extract port name for CTA
    port_name = extract_port_name_for_cta(page_name)
    
    # Format content
    content_html = format_content_html(full_content)
    
    # Generate breadcrumb text
    breadcrumb_text = page_name
    
    # Split H1 for styling (make last word italic in span)
    h1_parts = h1.split()
    if len(h1_parts) > 1:
        h1_html = f"{' '.join(h1_parts[:-1])} <span>{h1_parts[-1]}</span>"
    else:
        h1_html = h1
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="ship chandler, ship supply, provisions, marine stores, bonded stores, deck stores, engine stores, vessel supply, marine procurement">
  <meta name="author" content="Ship Chandler Libya CO., LTD">
  
  <!-- Open Graph Meta Tags -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:type" content="website">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&display=swap" rel="stylesheet">
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">

  <!-- Port Pages CSS -->
  <link rel="stylesheet" href="../assets/css/port-pages.css">
</head>
<body>

  <!-- HEADER / NAVBAR -->
  <header class="site-header" id="site-header">
    <div class="header-inner">
      <a class="logo" href="../index.html">
        <img src="../assets/imgs/logo.png" alt="ShipChandler Nigeria Logo" width="36" height="36">
        <span class="logo-text">
          <strong>ShipChandler</strong>
          <span>Nigeria</span>
        </span>
      </a>

      <button class="nav-toggle" type="button" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>

      <nav class="primary-nav" id="primary-nav">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>
          <li class="nav-item has-dropdown">
            <a class="nav-link" href="../services.html">Services <span class="nav-arrow"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></span></a>
            <div class="dropdown-menu">
              <a href="../services.html#provisions">Provisions Supply</a>
              <a href="../services.html#deck">Deck Stores</a>
              <a href="../services.html#cabin">Cabin & Galley</a>
              <a href="../services.html#engine">Engine Stores</a>
              <a href="../services.html#bonded">Bonded Stores</a>
              <a href="../services.html#safety">Safety & PPE</a>
            </div>
          </li>
          <li class="nav-item has-dropdown">
            <a class="nav-link" href="javascript:void(0)">Ports <span class="nav-arrow"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></span></a>
            <div class="mega-menu">
              <div class="mega-header">
                <div class="mega-header-title">Nigerian & African Port Network</div>
                <div class="mega-search">
                  <i class="fas fa-search" style="color:var(--gray-400);"></i>
                  <input type="text" id="mega-port-search" placeholder="Search ports...">
                </div>
              </div>
              <div class="mega-grid" id="mega-port-list">
                <!-- Populated via JS -->
              </div>
            </div>
          </li>
          <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
        </ul>
        <a class="btn btn-primary" style="padding: 10px 24px; font-size: 0.8rem;" href="../request-quote.html">Get Quote</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- PORT HERO - EDITORIAL SPLIT -->
    <section class="port-hero">
      <img src="../assets/imgs/nigeria-port-ship-image-portrait.jpg" alt="{page_name}" class="port-hero-bg">
      <div class="container">
        <div class="port-hero-content">
          <ul class="breadcrumb">
            <li><a href="../index.html">Home</a></li>
            <li><span>/</span></li>
            <li><a href="../index.html#ports">Ports</a></li>
            <li><span>/</span></li>
            <li style="color: rgba(255,255,255,0.7);">{breadcrumb_text}</li>
          </ul>
          <span class="hero-eyebrow">Professional Marine Supply</span>
          <h1 class="hero-title">{h1_html}</h1>
          <p class="hero-desc">{meta_description}</p>
        </div>
      </div>
    </section>

    <!-- ARTICLE CONTENT SECTION -->
    <section class="article-section">
      <div class="container">
        <div class="article-container">
          <article class="article-content">
{content_html}

            <!-- Article CTA -->
            <div class="article-cta">
              <h3>Need Supply at {port_name}?</h3>
              <p>Send us your complete vessel requisition and our team will respond with a competitive quotation.</p>
              <a href="../request-quote.html" class="btn btn-primary">Request a Quote <i class="fas fa-arrow-right"></i></a>
            </div>
          </article>
        </div>
      </div>
    </section>
  </main>

  <!-- FOOTER - MINIMAL & UNIQUE -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="logo" href="../index.html">
            <img src="../assets/imgs/logo.png" alt="Logo" width="36" height="36">
            <span class="logo-text">
              <strong>ShipChandler</strong>
              <span>Nigeria</span>
            </span>
          </a>
          <p>SHIP CHANDLER NIGERIA CO., LTD is a licensed marine supplier providing provisions, technical
            stores, bonded goods and emergency vessel supply across all Nigerian ports and anchorages.</p>
        </div>

        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul class="footer-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../about.html">About Us</a></li>
            <li><a href="../services.html">Services</a></li>
            <li><a href="../contact.html">Contact</a></li>
            <li><a href="../request-quote.html">Request a Quote</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Services</h4>
          <ul class="footer-links">
            <li><a href="../services.html#provisions">Provisions Supply</a></li>
            <li><a href="../services.html#bonded">Bonded Stores</a></li>
            <li><a href="../services.html#deck">Deck Stores</a></li>
            <li><a href="../services.html#engine">Engine Stores</a></li>
            <li><a href="../services.html#safety">Safety & PPE</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Contact Us</h4>
          <ul class="footer-contact-list">
            <li><i class="fas fa-map-marker-alt"></i> Lagos Port Complex, Wharf Road, Apapa, Lagos, Nigeria</li>
            <li><i class="fas fa-envelope"></i> <a href="mailto:sales@shipchandlernigeria.com">sales@shipchandlernigeria.com</a></li>
            <li><i class="fas fa-user-tie"></i> Ibrahim Adeyemi</li>
            <li>
              <a class="hero-whatsapp-bar" href="https://wa.me/2482743244" target="_blank" rel="noopener noreferrer"
                aria-label="Direct WhatsApp contact (+248) 2 743 244">
                <span class="hero-whatsapp-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path
                      d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                  </svg>
                </span>
                <span class="hero-whatsapp-tag">WhatsApp:</span>
                <span class="hero-whatsapp-num">(+248) 2 743 244</span>
                <span class="hero-whatsapp-arrow" aria-hidden="true">&rarr;</span>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 SHIP CHANDLER NIGERIA CO., LTD. All rights reserved.</div>
      </div>
    </div>
  </footer>

  <!-- FLOATING WHATSAPP -->
  <a href="https://wa.me/2482743244" class="whatsapp-float" target="_blank" rel="noopener noreferrer"
    aria-label="WhatsApp Contact +248 2 743 244">
    <i class="fab fa-whatsapp"></i>
  </a>

  <script src="../assets/js/port-pages.js"></script>
</body>
</html>
'''
    
    return filename, html_template

def main():
    """Main function to generate all port pages"""
    print(f"Reading Excel file: {EXCEL_PATH}")
    
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
        print(f"Found {len(df)} pages to generate")
        
        # Create output directory if it doesn't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        port_list = []
        
        # Generate each page
        for idx, row in df.iterrows():
            try:
                filename, html_content = generate_page_html(row)
                output_path = OUTPUT_DIR / filename
                
                # Write the file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                generated_files.append(filename)
                port_list.append(str(row['Page Name']))
                
                print(f"  ✓ Generated: {filename}")
                
            except Exception as e:
                print(f"  ✗ Error generating page {idx + 1}: {str(e)}")
                continue
        
        print(f"\n✓ Successfully generated {len(generated_files)} port pages!")
        print(f"✓ Files saved to: {OUTPUT_DIR}")
        
        # Generate ports list for JavaScript
        print("\n" + "="*60)
        print("Port names for JavaScript navigation:")
        print("="*60)
        for port in sorted(port_list):
            print(f'  "{port}",')
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
