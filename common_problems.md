### Uninstall a module using the command line:

1. Run the following command in your shell

```bash
    ./odoo-bin shell -c /etc/odoo-server.conf -d db_name
```

2. Then run this Python script

```python
    self.env['ir.module.module'].search([('name', '=', 'module_name')]).button_immediate_uninstall()
```


### Clear Odoo cache
self.env.invalidate_all()
