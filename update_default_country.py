# update_country.py
def update_country(env, country_code):
    Company = env['res.company']
    Country = env['res.country']

    default_company = Company.search([], limit=1)
    country_to_set = Country.search([('code', '=', country_code)], limit=1)

    if default_company and country_to_set:
        default_company.write({'country_id': country_to_set.id})
        print(f"Updated the default company's country to {country_code}.")
    else:
        print("Could not update the country. Please check if the country code is correct and exists in the database.")

if __name__ == '__main__':
    # Assume that the script will receive the country code as the first argument.
    import sys
    country_code = sys.argv[1] if len(sys.argv) > 1 else 'US'  # Default to 'US' if no argument is provided.
    update_country(self.env, country_code)
