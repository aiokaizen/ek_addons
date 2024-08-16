// Override all page titles
// odoo.define('librarian.TitleServiceOverride', ['web.core', 'web.title_service'], function (require) {

//     'use strict';

//     const { ServiceProvider } = require('web.core');
//     const { TitleService } = require('web.title_service');

//     const CustomTitleService = TitleService.extend({
//         setTitle(title) {
//             // Prefix the title with 'CaisseMaster - '
//             const newTitle = `CaisseMaster - ${title}`;
//             this._super(newTitle);
//             alert("Overriding setTitle")
//         },
//     });

//     ServiceProvider.override('title', CustomTitleService);
// });


odoo.define('librarian.TitleServiceOverride', function (require) {

    'use strict';

    const TitleService = require('web.title_service');

    TitleService.include({
        setTitle: function (title) {
            title = title ? 'CaisseMaster - ' + title : 'CaisseMaster';
            this._super(title);
        },
    });
});



// Override POS title
odoo.define('librarian.PosTitleOverride', function (require) {

    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    const PosTitleOverride = (PosComponent) =>
        class extends PosComponent {
            mounted() {
                super.mounted();
                document.title = "CaisseMaster POS";
            }
        };

    Registries.Component.extend(PosComponent, PosTitleOverride);
});



// odoo.define('librarian.WebClientTitleOverride', function (require) {
//     'use strict';

//     const WebClient = require('web.WebClient');

//     WebClient.include({
//         set_title: function (title) {
//             title = title ? 'CaisseMaster - ' + title : 'CaisseMaster';
//             this._super(title);
//         }
//     });
// });