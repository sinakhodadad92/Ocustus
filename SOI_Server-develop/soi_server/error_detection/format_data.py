
def finalize_result(cropped_panels, component_errors, components_config):
    print("Format/finalize results\n")
    components = []
    for designator in component_errors:
        component = next((x for x in components_config if x["DESIGNATOR"] == designator), None)
        components.append({
            'designator': designator,
            'component_value': component['COMPONENT VALUE'],
            'errors': component_errors[designator]
        })


    # Format data
    result = {
        'cropped_panels': cropped_panels,
        'components': components
    }
    return result
