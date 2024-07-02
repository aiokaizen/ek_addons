# ----
# Description: This script deletes all Odoo test databases and deletes their respective filestores
# Author: EKBlocks
# Usage: . reset_test_dbs.sh
# ----

# Get the default filestore directory of the `odoo` user
FILESTORE="$(eval echo ~odoo)/.local/share/Odoo/filestore"

# List all databases with odoo and test keywords in them
DATABASES=$(sudo -u postgres psql -t -c "SELECT datname FROM pg_database WHERE datname LIKE '%odoo%test%';")

echo "$DATABASES" | while read -r db; do
    if [[ -n "$db" ]]; then
        db=$(echo "$db" | xargs)  # Trim any leading/trailing whitespace
        echo "Dropping database: $db;"
        sudo -u postgres psql -c "DROP DATABASE \"$db\";"
        sudo rm -rf $FILESTORE/$db
    fi
done
