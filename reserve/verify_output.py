import re
import json
import os
from bs4 import BeautifulSoup

def check_hyperlinks_in_output(output_path, json_path):
    """
    Analyzes the output text to verify if it contains proper hyperlinks to JSON data sources.
    
    Args:
        output_path (str): Path to the output text/HTML file
        json_path (str): Path to the JSON data file
    
    Returns:
        dict: Analysis results with hyperlink counts and quality assessment
    """
    # Read the output
    with open(output_path, 'r') as f:
        output_text = f.read()
    
    # Load JSON data
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Extract URLs from JSON
    json_urls = []
    json_titles = []
    json_dates = []
    
    # This assumes json_data is a list of articles or has an articles field
    # Adjust according to your actual JSON structure
    articles = json_data if isinstance(json_data, list) else json_data.get('articles', [])
    
    for article in articles:
        if 'url' in article:
            json_urls.append(article['url'])
        if 'title' in article:
            json_titles.append(article['title'])
        if 'publication_date' in article:
            json_dates.append(article['publication_date'])
    
    # Find all hyperlinks in HTML format
    html_link_pattern = r'<a\s+href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>'
    html_links = re.findall(html_link_pattern, output_text, re.IGNORECASE | re.DOTALL)
    
    # Find all hyperlinks in Markdown format
    md_link_pattern = r'\[(.*?)\]\((https?://[^\s)]+)\)'
    md_links = re.findall(md_link_pattern, output_text)
    
    # Combine all found links
    all_hrefs = [link[0] for link in html_links] + [link[1] for link in md_links]
    
    # Check if any of the found links match the JSON URLs
    matching_urls = [url for url in all_hrefs if any(json_url in url for json_url in json_urls)]
    
    # Parse HTML for deeper analysis if there's HTML content
    try:
        soup = BeautifulSoup(output_text, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraphs_text = [p.get_text() for p in paragraphs]
        paragraphs_with_links = [p for p in paragraphs if p.find('a')]
    except:
        # If not HTML or parsing fails, use regex to estimate paragraphs
        paragraphs_text = [p for p in re.split(r'<p>|</p>|\n\n', output_text) if p.strip()]
        paragraphs_with_links = [p for p in paragraphs_text if '<a href' in p or re.search(md_link_pattern, p)]
    
    # Prepare results
    results = {
        'total_paragraphs': len(paragraphs_text),
        'paragraphs_with_links': len(paragraphs_with_links),
        'html_links_found': len(html_links),
        'markdown_links_found': len(md_links),
        'total_links_found': len(html_links) + len(md_links),
        'matching_urls': len(matching_urls),
        'percent_paragraphs_with_links': len(paragraphs_with_links) / max(1, len(paragraphs_text)) * 100,
        'valid_embuild_urls': sum(1 for url in all_hrefs if 'embuildvlaanderen.be' in url),
        'links_include_dates': sum(1 for link_text in [link[1] for link in html_links] + [link[0] for link in md_links] 
                                 if re.search(r'\d{1,2}\s+[a-z]{3}\s+\d{4}', link_text, re.IGNORECASE))
    }
    
    # Print a summary
    print(f"Analyse van hyperlinks in de output:")
    print(f"- Totaal aantal alinea's: {results['total_paragraphs']}")
    print(f"- Alinea's met hyperlinks: {results['paragraphs_with_links']} ({results['percent_paragraphs_with_links']:.1f}%)")
    print(f"- HTML links gevonden: {results['html_links_found']}")
    print(f"- Markdown links gevonden: {results['markdown_links_found']}")
    print(f"- Totaal aantal links gevonden: {results['total_links_found']}")
    print(f"- Links die overeenkomen met JSON URL's: {results['matching_urls']}")
    print(f"- Geldige Embuild Vlaanderen URL's: {results['valid_embuild_urls']}")
    print(f"- Links met datums: {results['links_include_dates']}")
    
    # Sample of links found
    if html_links:
        print("\nVoorbeelden van gevonden HTML links:")
        for i, link in enumerate(html_links[:3]):
            print(f"  {i+1}. <a href='{link[0]}'>{link[1]}</a>")
    
    if md_links:
        print("\nVoorbeelden van gevonden Markdown links:")
        for i, link in enumerate(md_links[:3]):
            print(f"  {i+1}. [{link[0]}]({link[1]})")
    
    # Assessment and recommendations
    print("\nBEOORDELING:")
    
    if results['total_links_found'] < 3:
        print("❌ ONVOLDOENDE LINKS: De output bevat minder dan 3 hyperlinks.")
        print("   AANBEVELING: Pas de prompt aan om de noodzaak van meerdere hyperlinks te benadrukken.")
    else:
        print("✅ VOLDOENDE LINKS: De output bevat 3 of meer hyperlinks.")
    
    if results['percent_paragraphs_with_links'] < 50:
        print("❌ LAGE LINK DEKKING: Minder dan de helft van de alinea's bevat hyperlinks.")
        print("   AANBEVELING: Vraag om links in meer alinea's.")
    else:
        print("✅ GOEDE LINK DEKKING: Ten minste de helft van de alinea's bevat hyperlinks.")
    
    if results['valid_embuild_urls'] < results['total_links_found'] * 0.8:
        print("❌ ONGELDIGE URL'S: Veel links verwijzen niet naar het Embuild Vlaanderen domein.")
        print("   AANBEVELING: Benadruk het gebruik van de exacte URL's uit de JSON-data.")
    else:
        print("✅ GELDIGE URL'S: De meeste links verwijzen naar het Embuild Vlaanderen domein.")
    
    if results['links_include_dates'] < results['total_links_found'] * 0.8:
        print("❌ ONTBREKENDE DATUMS: In veel linkteksten ontbreken publicatiedatums.")
        print("   AANBEVELING: Benadruk het opnemen van datums in de linktekst.")
    else:
        print("✅ GOEDE DATUM INCLUSIE: De meeste linkteksten bevatten publicatiedatums.")
        
    return results

def run_verification(base_path):
    """
    Runs the verification on the generated output.
    
    Args:
        base_path (str): Base path for the project
    """
    output_path = f"{base_path}/data/output.txt"
    json_path = f"{base_path}/data/emv_pers.json"
    
    if not os.path.exists(output_path):
        print(f"Fout: Output bestand niet gevonden op {output_path}")
        return
    
    if not os.path.exists(json_path):
        print(f"Fout: JSON bestand niet gevonden op {json_path}")
        return
    
    print(f"Verificatie starten voor output: {output_path}")
    print(f"Vergelijken met JSON data: {json_path}")
    print("=" * 80)
    
    results = check_hyperlinks_in_output(output_path, json_path)
    
    print("=" * 80)
    
    # Overall recommendation
    print("\nALGEMENE BEOORDELING:")
    score = 0
    if results['total_links_found'] >= 3:
        score += 1
    if results['percent_paragraphs_with_links'] >= 50:
        score += 1
    if results['valid_embuild_urls'] >= results['total_links_found'] * 0.8:
        score += 1
    if results['links_include_dates'] >= results['total_links_found'] * 0.8:
        score += 1
    
    if score == 4:
        print("🌟 UITSTEKEND: Het persbericht voldoet aan alle vereisten voor hyperlinks.")
    elif score == 3:
        print("✅ GOED: Het persbericht voldoet aan de meeste vereisten voor hyperlinks.")
    elif score == 2:
        print("⚠️ VOLDOENDE: Het persbericht voldoet aan sommige vereisten, maar heeft verbetering nodig.")
    else:
        print("❌ ONVOLDOENDE: Het persbericht moet worden verbeterd op het gebied van hyperlinks.")

if __name__ == "__main__":
    base_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow"
    run_verification(base_path)