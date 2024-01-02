from web_interface.private.components.make_css_style_sheet_link_html import make_css_style_sheet_link_html
from web_interface.private.components.make_footer_center_html import make_footer_center_html
from web_interface.private.components.make_header_main_footer_html import make_header_main_footer_html
from web_interface.private.components.make_html_file import make_html_file
from web_interface.private.features.make_public_page_html import make_public_page_html
from web_interface.private.features.make_sign_in_form_html import make_login_form_html


def make_sign_in_page() -> str:
    return make_html_file(
        title="Developer Dashboard | Sign In",
        headers=[
            make_css_style_sheet_link_html(file_name="flex-box.css"),
        ],
        body=[
            make_header_main_footer_html(
                header=make_public_page_html(),
                main=make_login_form_html(link_to_register_form="/register"),
                footer=make_footer_center_html()
            ),
        ]
    )
