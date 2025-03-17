import os
from google import genai
from google.genai import types
from google.colab import userdata

def generate():
    api_key = userdata.get('AI_STUDIO_API')
    client = genai.Client(api_key=api_key)

    file_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow/data/emv_pers.json"
    files = [
        client.files.upload(file=file_path),
    ]
    model = "gemini-2.0-flash-thinking-exp-01-21"

    # Lees de user prompt uit het bestand
    prompt_file_path = "/content/drive/MyDrive/Colab Notebooks/publish_flow/user_input/prompt_1.txt"
    try:
        with open(prompt_file_path, "r") as f:
            user_prompt = f.read().strip()  # Lees en verwijder eventuele witruimte
    except FileNotFoundError:
        print(f"Bestand niet gevonden: {prompt_file_path}")
        return  # Stop de functie als het bestand niet bestaat

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text=user_prompt),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=64,
        max_output_tokens=65536,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Je hebt toegang tot een databank met nieuwsartikelen, elk opgeslagen als een JSON-object. De structuur van elk JSON-object bevat onder andere de volgende velden:
url: De volledige URL van het artikel.
publication_date: De publicatiedatum (bv. \"06 nov 2024\").
title: De kop of hoofdtitel van het artikel.
subheading: Een subkop of korte toelichting.
meta_description: Een korte omschrijving van het artikel.
og_image: Een link naar een representatieve afbeelding.
content: De hoofdtekst van het artikel, inclusief paragrafen, citaten en lijsten.
csv_metadata: Eventuele extra metadata die oorspronkelijk uit een CSV is gehaald (zoals originele datum of omschrijving).
Werkwijze:

Input en Databronnen:
Je ontvangt als input een stelling of bewering (bijv. \"De bouwsector moet meer investeren in waterbestendige stadsontwikkeling\"). Voordat je begint met schrijven, doorzoek je alle JSON-artikelen naar relevante feiten, cijfers en argumenten die betrekking hebben op de stelling. Deze gegevens dienen als onderbouwing van je uiteindelijke artikel.

Schrijf een Persartikel:
Op basis van de relevante informatie uit de JSON-databronnen schrijf je een nieuw persartikel dat een reactie geeft op de inputstelling. Het doel is om een persartikel te schrijven voor Embuild Vlaanderen. Je gebruikt de json-artikel als inspiratie om een standpunt te formuleren. Je zorgt dat je geen loutere samenvatting geeft, maar dat de standpunten van Embuild Vlaanderen centraal staan. Maak telkens ook een citaat van Caroline Deiteren op, je mag dit citaat zelf opmaken op basis van wat je denkt dat Caroline zou willen toevoegen. Het artikel moet:

Een duidelijke kop (headline) en, indien gewenst, een subkop bevatten.
Een introductie waarin de kern van de stelling kort wordt geïntroduceerd.
Een hoofdtekst met meerdere paragrafen waarin je de argumenten en feiten samenvoegt.
Een afsluiting die de boodschap kracht bijzet.
Literaire Stijl en Layout:

Stijl: Schrijf in een journalistieke, feitelijke en formele stijl, vergelijkbaar met de bestaande persartikelen in de JSON-databron. Gebruik heldere taal, concrete cijfers en zorg voor een objectieve toon.
Layout:
Begin met een duidelijke kop (bijv. als <h1> of als hoofdregel).
Voeg een subkop toe onder de kop.
Gebruik meerdere paragrafen voor de hoofdtekst.
Indien relevant, gebruik blokcitaten of lijsten om belangrijke gegevens te benadrukken.
Inline Metadata: Wanneer je cijfers, statistieken of specifieke feiten noemt, vermeld dan direct de herkomst door de bijbehorende metadata inline te integreren. Bijvoorbeeld: \"Volgens de notarisbarometer (publicatiedatum: 06 nov 2024, uit 'Uitstel woonwaarborg slechte zaak voor huishoudens en bouwsector') kost een nieuw appartement in Vlaanderen gemiddeld 349.210 euro.\"
Cijfers en Statistieken:
Je mag gerust cijfers en statistieken gebruiken om je argumenten te ondersteunen. Zorg er echter voor dat elke keer dat je een cijfer noemt, je de broninformatie (zoals publicatiedatum, titel en/of andere relevante metadata) direct meegeeft in de tekst, zodat de lezer kan nagaan waar de informatie vandaan komt.

Voorbeeld Input:
Stel dat de input de volgende stelling is:
\"De bouwsector moet meer investeren in waterbestendige stadsontwikkeling om overstromingsrisico's te beperken.\"
Jouw taak is om door de JSON-artikelen te zoeken naar relevante feiten (bijvoorbeeld over overstromingskansen, investeringsbedragen, statistieken over wateroverlast) en een nieuw persartikel te schrijven dat deze stelling bespreekt en onderbouwt.


Vermeld altijd inline de metadata (zoals publicatiedatum en bron) wanneer je cijfers of statistieken gebruikt, zodat de informatie controleerbaar is.
Hanteer een consistente layout die past bij de bestaande persartikelen."""),
        ],
    )

    output_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output_text += chunk.text
        print(chunk.text, end="")

    return output_text

if __name__ == "__main__":
    output = generate()

    # Opslaan in een bestand
    with open("output.txt", "w") as f:
        f.write(output)
    print("\nOutput opgeslagen in output.txt")