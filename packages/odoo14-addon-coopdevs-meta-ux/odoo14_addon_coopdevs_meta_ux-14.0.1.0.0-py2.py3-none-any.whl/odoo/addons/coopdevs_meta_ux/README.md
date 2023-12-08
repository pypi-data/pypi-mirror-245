# Coopdevs Meta UX Improvements

This module is designed to improve the quality of life for Odoo developers, administrators and users. It provides a mechanism to automatically install a set of useful modules from the OCA (Odoo Community Association) and other sources.

## Features

- Automatic installation of modules: Just add the module names to the `__manifest__.py` file and they will be installed when the `coopdevs_meta_ux` module is installed or upgraded.

## Modules Included

This module installs the following modules:

| Module | Description | Repository |
| --- | --- | --- |
| `web_search_with_and` | Enhances the search functionality by allowing AND conditions in search. | [Link](https://github.com/OCA/web/tree/14.0/web_search_with_and) |
| `web_remember_tree_column_width` | Remembers the width of the columns in tree view. | [Link](https://github.com/OCA/web/tree/14.0/web_remember_tree_column_width) |
| `web_refresher` | Adds a refresh button to the view. | [Link](https://github.com/OCA/web/tree/14.0/web_refresher) |
| `web_group_expand` | Allows expanding and collapsing groups in tree view. | [Link](https://github.com/OCA/web/tree/14.0/web_group_expand) |
| `web_advanced_search` | Provides advanced search features. | [Link](https://github.com/OCA/web/tree/14.0/web_advanced_search) |
| `web_access_rule_buttons` | Shows access rules on buttons. | [Link](https://github.com/OCA/web/tree/14.0/web_access_rule_buttons) |
| `web_widget_datepicker_fulloptions` | Provides a date picker with full options. | [Link](https://github.com/OCA/web/tree/14.0/web_widget_datepicker_fulloptions) |
| `web_widget_numeric_step` | Provides a numeric step widget. | [Link](https://github.com/OCA/web/tree/14.0/web_widget_numeric_step) |
| `web_widget_open_tab` | Allows opening records in new browser tabs. | [Link](https://github.com/OCA/web/tree/14.0/web_widget_open_tab) |
| `base_archive_date` | Adds a date field to the archive functionality. | [Link](https://github.com/OCA/server-ux/tree/14.0/base_archive_date) |
| `base_custom_filter` | Provides custom filters. | [Link](https://github.com/OCA/server-ux/tree/14.0/base_custom_filter) |
| `base_export_manager` | Enhances the export functionality. | [Link](https://github.com/OCA/server-ux/tree/14.0/base_export_manager) |
| `base_optional_quick_create` | Makes the quick create option optional. | [Link](https://github.com/OCA/server-ux/tree/14.0/base_optional_quick_create) |
| `base_user_locale` | Allows setting a locale for each user. | [Link](https://github.com/OCA/server-ux/tree/14.0/base_user_locale) |
| `date_range` | Provides a date range feature. | [Link](https://github.com/OCA/server-ux/tree/14.0/date_range) |
| `date_range_account` | Adds date range support to accounting. | [Link](https://github.com/OCA/server-ux/tree/14.0/date_range_account) |
| `filter_multi_user` | Allows applying filters to multiple users. | [Link](https://github.com/OCA/server-ux/tree/14.0/filter_multi_user) |
| `mass_editing` | Provides a mass editing feature. | [Link](https://github.com/OCA/server-ux/tree/14.0/mass_editing) |
| `sequence_reset_period` | Allows resetting sequences based on a period. | [Link](https://github.com/OCA/server-ux/tree/14.0/sequence_reset_period) |
| `report_qweb_element_page_visibility` | Allows hiding elements in reports based on page visibility. | [Link](https://github.com/OCA/reporting-engine/tree/14.0/report_qweb_element_page_visibility) |

## Publishing Pypi releases with CI/CD

To trigger a new release with this pipeline, you need to tag a commit. Here's a quick step-by-step guide:

1. Make the necessary changes to your Odoo modules. If you want to release more than one module, one way to do this is to create a commit that modifies the `__manifest__.py` files, updating the version number for each module you want to publish. This will ensure that the pipeline recognizes these modules as "modified" and includes them in the release.

2. After committing your changes, create a new tag.

3. Once the tag is pushed to your repository, GitLab will automatically start the pipeline. The pipeline will install necessary dependencies, prepare, build, and upload each modified module to PyPI.

4. Monitor the pipeline's progress in GitLab's CI/CD interface. If everything goes well, your new release should be available on PyPI once the pipeline completes.

Remember, only the modules that were modified in the commit associated with the tag will be released to PyPI. If no modules were modified, the pipeline will still run, but no new releases will be made.
