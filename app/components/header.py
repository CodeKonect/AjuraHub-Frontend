from nicegui import ui
from app.services.auth_utils import is_authenticated, get_current_user, logout


def add_global_styles():
    """Add global Tailwind + brand styles (call once per page)."""
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        *:not(.material-icons):not(.q-icon):not([class*="material-icons"]):not(i) {
            font-family: 'Raleway', sans-serif !important;
        }

        .material-icons {
            font-family: 'Material Icons' !important;
            font-size: 24px;
            line-height: 1;
        }

        header {
            background-color: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(8px) !important;
            border-bottom: 1px solid #e5e7eb !important;
            position: fixed !important;
            top: 0 !important;
            z-index: 1000 !important;
            height: 64px !important;
        }

        .q-btn, button {
            font-family: 'Raleway', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
        }

        .bg-blue-600 { background-color: #0055B8 !important; color: white !important; }
        .bg-blue-600:hover { background-color: #004494 !important; }

        .bg-gray-200 { background-color: #f3f4f6 !important; color: #1f2937 !important; }
        .bg-gray-200:hover { background-color: #e5e7eb !important; }

        .top-nav-link {
            color: #334155 !important;
            font-weight: 600 !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            text-decoration: none !important;
            transition: color .2s ease, background .2s ease !important;
        }
        .top-nav-link:hover { color: #0f172a !important; background: #f8fafb !important; }

        .nav-active {
            color: #0055B8 !important;
            font-weight: 700 !important;
            position: relative;
        }
        .nav-active::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            right: 0;
            height: 3px;
            background-color: #0055B8;
            border-radius: 2px;
        }

        .dropdown-hover { position: relative; }
        .dropdown-hover .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            padding: 8px 0;
            min-width: 200px;
            z-index: 1000;
        }
        .dropdown-hover:hover .dropdown-content { display: block; }

        .dropdown-content a {
            display: block;
            padding: 12px 16px;
            color: #374151;
            text-decoration: none;
            font-family: 'Raleway', sans-serif;
            font-weight: 400;
            transition: background-color 0.2s ease;
        }
        .dropdown-content a:hover {
            background-color: #f3f4f6;
            color: #0055B8;
        }

        .dropdown-content a.active {
            background-color: #f0f8ff !important;
            color: #0055B8 !important;
            font-weight: 500 !important;
            border-left: 3px solid #0055B8;
            padding-left: 13px !important;
        }
    </style>
    ''')


def header(current_page: str = ''):
    """Global header component with active navigation, auth, and dropdowns."""
    add_global_styles()

    with ui.element('header').classes(
        'fixed top-0 left-0 right-0 z-50 w-full h-16 px-4 shadow-md border-b flex items-center justify-between bg-white/90 backdrop-blur'
    ):

        # --- Left: Logo ---
        with ui.row().classes('items-center gap-3 cursor-pointer').on('click', lambda: ui.navigate.to('/')):
            ui.icon('hub', size='2rem').style('color: #0055B8 !important;')
            ui.label('Dompell').classes('text-xl font-semibold text-gray-900')

        # --- Center Placeholder (for future menus) ---
        with ui.row().classes('flex items-center gap-4').style('position: absolute; left: 50%; transform: translateX(-50%);'):
            pass

        # --- Right: Navigation and Auth ---
        with ui.row().classes('flex items-center gap-4'):
            # Determine active links
            def is_active(path): return current_page.startswith(path)
            home_class = 'nav-active' if current_page == '/' else ''
            about_class = 'nav-active' if current_page == '/about' else ''
            how_class = 'nav-active' if is_active('/how-it-works') else ''
            resources_active = any(is_active(p) for p in ['/contact', '/help-and-support', '/training-program-directory'])

            # Top links
            ui.link('Home', '/').classes(f'top-nav-link {home_class}')
            ui.link('About Us', '/about').classes(f'top-nav-link {about_class}')
            ui.link('How it works', '/how-it-works').classes(f'top-nav-link {how_class}')

            # --- Resources Dropdown ---
            resources_classes = 'dropdown-hover dropdown-active' if resources_active else 'dropdown-hover'
            with ui.element('div').classes(resources_classes).style('padding: 8px 16px;'):
                label_style = 'font-weight: 600; color: #0055B8;' if resources_active else 'font-weight: 500; color: #4b5563;'
                icon_style = 'color: #0055B8;' if resources_active else 'color: #4b5563;'
                with ui.row().classes('items-center gap-1 cursor-pointer'):
                    ui.label('Resources').style(label_style)
                    ui.icon('arrow_drop_down').classes('dropdown-icon').style(icon_style)

                # Dropdown content
                resource_links = [
                    {'name': 'Contact Us', 'path': '/contact'},
                    {'name': 'Trainings/Bootcamps', 'path': '/training-program-directory'},
                    {'name': 'Success Stories', 'path': '/candidates/success-stories'},
                    {'name': 'Help & Support', 'path': '/help-and-support'},
                ]

                html_string = f'''
                <div class="flex flex-col p-2">
                    {''.join(
                        f'<a href="{link["path"]}" class="nav-dropdown-btn {"active" if current_page == link["path"] else ""}">{link["name"]}</a>'
                        for link in resource_links
                    )}
                </div>
                '''

                # ✅ Fixed sanitize issue
                ui.html(html_string, sanitize=False)

            # --- Authentication Buttons ---
            if not is_authenticated():
                ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes(
                    'bg-white border text-blue-600 border-blue-600 hover:bg-blue-50'
                )
                ui.button('Register', on_click=lambda: ui.navigate.to('/login?tab=Sign+Up')).classes('bg-blue-600 text-white')
            else:
                user = get_current_user() or {}
                user_name = user.get('name', user.get('email', 'User'))
                user_role = user.get('role', 'USER')

                with ui.row().classes('items-center gap-4'):
                    ui.icon('notifications', size='1.5rem').classes('cursor-pointer text-gray-600 hover:text-blue-600')

                    with ui.menu() as menu:
                        if user_role == 'ADMIN':
                            ui.menu_item('Admin Dashboard', on_click=lambda: ui.navigate.to('/admin/dashboard'))
                        elif user_role == 'TRAINEE':
                            ui.menu_item('My Dashboard', on_click=lambda: ui.navigate.to('/candidates/dashboard'))
                        elif user_role == 'EMPLOYER':
                            ui.menu_item('Employer Dashboard', on_click=lambda: ui.navigate.to('/employers/dashboard'))
                            ui.menu_item('Job Postings', on_click=lambda: ui.navigate.to('/employer/job-posting'))

                        ui.menu_item('Profile Settings', on_click=lambda: ui.navigate.to('/settings/profile'))
                        ui.separator()
                        ui.menu_item(f'Logout ({user_name})', on_click=logout)

                    # --- Profile Icon ---
                    profile_pic_url = user.get('traineeProfile', {}).get('profilePictureUrl', '') if user else ''
                    if profile_pic_url:
                        with ui.element('div').style(
                            'width:36px;height:36px;border-radius:50%;overflow:hidden;border:2px solid #0055B8;cursor:pointer;'
                            'box-shadow:0 2px 6px rgba(0,0,0,0.15);'
                        ).on('click', menu.open):
                            ui.image(profile_pic_url).style('width:100%;height:100%;object-fit:cover;')
                    else:
                        initials = ''.join([n[0].upper() for n in user_name.split()[:2]])
                        with ui.element('div').style(
                            'width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#0055B8,#0066CC);'
                            'color:white;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:14px;'
                            'cursor:pointer;box-shadow:0 2px 6px rgba(0,85,184,0.3);'
                        ).on('click', menu.open):
                            ui.label(initials)
