#!/bin/bash

# -----------------------------------------------------
#   This script drops an odoo demo database with the name of
#   'odoo_demo_db' and then recreates it.
#   It takes as an argument -l (local) to specify the default
#   language of the database, possible values are: en, ar, fr
# -----------------------------------------------------

# Variables
DB_TO_DROP="odoo_demo_db"
DB_TO_CREATE="odoo_demo_db"
DB_USER="$(whoami)"

DB_ENCODING="UTF8"  # Adjust the encoding as needed
DB_COLLATE="en_US.utf8"  # Adjust the collation as needed
DB_CTYPE="en_US.utf8"  # Adjust the character type as needed
DB_TEMPLATE="template0"  # Default template

# Process command line options
while getopts "l:" opt; do
  case ${opt} in
    l )
      LOCALE=$OPTARG
      case ${LOCALE} in
        en)
          DB_COLLATE="en_US.utf8"
          DB_CTYPE="en_US.utf8"
          ;;
        fr)
          DB_COLLATE="fr_FR.utf8"
          DB_CTYPE="fr_FR.utf8"
          ;;
        ar)
          DB_COLLATE="ar_SA.utf8"
          DB_CTYPE="ar_SA.utf8"
          ;;
        *)
          echo "Invalid locale. Supported locales are en, fr, and ar."
          exit 1
          ;;
      esac
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      ;;
  esac
done
shift $((OPTIND -1))


# Drop the existing database
echo "Dropping the database: $DB_TO_DROP"
dropdb -U $DB_USER $DB_TO_DROP --if-exists

# Check if dropdb was successful
if [ $? -eq 0 ]; then
    echo "Database $DB_TO_DROP dropped successfully."
else
    echo "Failed to drop the database $DB_TO_DROP. Exiting."
    exit 1
fi

# Create a new database with specific attributes
echo "Creating the database: $DB_TO_CREATE"
createdb -U $DB_USER -E $DB_ENCODING --lc-collate=$DB_COLLATE --lc-ctype=$DB_CTYPE -T $DB_TEMPLATE $DB_TO_CREATE


# Check if createdb was successful
if [ $? -eq 0 ]; then
    echo "Database $DB_TO_CREATE created successfully."
else
    echo "Failed to create the database $DB_TO_CREATE."
    exit 1
fi

# Choose the default country of the database
../odoo-bin shell -d $DB_TO_CREATE --script=./update_country.py --args="'$COUNTRY_CODE'"
