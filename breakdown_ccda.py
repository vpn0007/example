import xmltodict
import os

def extract_and_save_components(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        xml_data = xmltodict.parse(f.read(), dict_constructor=dict)

    # Extract main ClinicalDocument structure
    clinical_doc = xml_data.get("ClinicalDocument", {})
    structured_body = clinical_doc.get("component", {}).get("structuredBody", {})
    components = structured_body.get("component", [])

    if not isinstance(components, list):  # Ensure it's a list
        components = [components]

    if input_file=="base_ccda.xml":
        output_dir = "extracted_sections_base"
    elif input_file == "compare_ccda.xml":
        output_dir = "extracted_sections_compare"
    os.makedirs(output_dir, exist_ok=True)  # Create directory to store extracted files

    extracted_components = []  # Store extracted components for later removal

    for comp in components:
        title = comp.get("section", {}).get("title")
        if title:
            filename = f"{output_dir}/{title.replace(' ', '_')}.xml"  # Replace spaces with underscores
            with open(filename, "w", encoding="utf-8") as f:
                f.write(xmltodict.unparse({"ClinicalDocument": {"component": comp}}, pretty=True))
            extracted_components.append(comp)  # Store extracted component

    # Remove extracted components to keep the remaining structure
    for comp in extracted_components:
        components.remove(comp)

    # Save remaining structure (header)
    header_file = f"{output_dir}/header.xml"
    with open(header_file, "w", encoding="utf-8") as f:
        f.write(xmltodict.unparse({"ClinicalDocument": clinical_doc}, pretty=False))




