from nicegui import ui
from app.services.auth_utils import is_authenticated, get_current_user, logout

def add_global_styles():
    """Add global styles - call this once per page that needs it"""
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Brand typography - excludes icons to prevent font override */
        *:not(.material-icons):not(.q-icon):not([class*="material-icons"]):not(i) {
            font-family: 'Raleway', sans-serif !important;
        }

        /* Material Icons properties */
        .material-icons {
            font-family: 'Material Icons' !important;
            font-weight: normal;
            font-style: normal;
            font-size: 24px;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
            font-feature-settings: 'liga';
            -webkit-font-smoothing: antialiased;
            -webkit-font-feature-settings: 'liga';
        }

        /* Ensure header styling takes precedence */
        header {
            background-color: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(8px) !important;
            border-bottom: 1px solid #e5e7eb !important;
        }

        /* Button styling protection */
        .q-btn, button {
            font-family: 'Raleway', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
        }

        /* Primary button styles */
        .bg-blue-600 {
            background-color: #0055B8 !important;
            color: white !important;
        }
        
        .bg-blue-600:hover, .hover\\:bg-blue-700:hover {
            background-color: #004494 !important;
        }

        /* Secondary button styles */
        .bg-gray-200 {
            background-color: #f3f4f6 !important;
            color: #1f2937 !important;
        }

        .bg-gray-200:hover, .hover\\:bg-gray-300:hover {
            background-color: #e5e7eb !important;
        }

        /* Danger button styles */
        .bg-red-600 {
            background-color: #dc2626 !important;
            color: white !important;
        }

        .bg-red-600:hover, .hover\\:bg-red-700:hover {
            background-color: #b91c1c !important;
        }

        .nicegui-content,
        .nicegui-column {
            display: block !important;
            flex-direction: unset !important;
            align-items: unset !important;
            gap: 0 !important;
            padding: 0 !important;
        }

        /* Typography classes */
        .heading-1 { font-size: 3rem; font-weight: 700; line-height: 1.1; }
        .heading-2 { font-size: 2.25rem; font-weight: 600; line-height: 1.2; }
        .sub-heading { font-size: 1.5rem; font-weight: 500; line-height: 1.4; }
        .body-text { font-size: 1rem; font-weight: 400; line-height: 1.6; }
        .button-label { font-size: 0.875rem; font-weight: 600; }
        .caption { font-size: 0.75rem; font-weight: 400; }

        /* Brand colors */
        .brand-primary { color: #0055B8; }
        .brand-charcoal { color: #1A1A1A; }
        .brand-slate { color: #4D4D4D; }
        .brand-light-mist { background-color: #F2F7FB; }
        .brand-primary-bg { background-color: #0055B8; }

        /* Content spacing to prevent overlap with fixed header */
        .main-content {
            margin-top: 4rem !important; /* 64px to match header height */
            padding-top: 1rem !important;
        }

        /* Ensure all page containers have proper spacing */
        .q-page, .page-container, .nicegui-content > div:first-child {
            margin-top: 4rem !important;
        }

        /* Override any conflicting padding/margin on main content areas */
        .nicegui-content .q-page-container,
        .nicegui-content > .q-column,
        .nicegui-content > div.flex.flex-col {
            padding-top: 4rem !important;
        }

        /* Fix header overlap issue - increase pt-20 to account for fixed header */
        .pt-20 {
            padding-top: 4.375rem !important; /* 70px - 64px header + 6px spacing */
        }

        /* Ensure header stays fixed and doesn't interfere with content */
        header {
            position: fixed !important;
            top: 0 !important;
            z-index: 1000 !important;
            height: 64px !important;
        }

        /* Menu styles */
        .q-menu {
            background: white !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
            padding: 8px 0 !important;
            min-width: 200px !important;
        }

        .q-item {
            padding: 12px 16px !important;
            color: #374151 !important;
            font-family: 'Raleway', sans-serif !important;
            font-weight: 400 !important;
            transition: background-color 0.2s ease !important;
            cursor: pointer !important;
        }

        .q-item:hover {
            background-color: #f3f4f6 !important;
            color: #0055B8 !important;
        }

        /* Hover dropdown styles */
        .dropdown-hover {
            position: relative;
        }

        .dropdown-hover .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            padding: 8px 0;
            min-width: 200px;
            z-index: 1000;
        }

        .dropdown-hover:hover .dropdown-content {
            display: block;
        }

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

        /* Navigation button styles */
        .nav-dropdown-btn {
            background: transparent !important;
            border: none !important;
            color: #334155 !important; /* slate-700 */
            font-weight: 600 !important;
            font-family: 'Raleway', sans-serif !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }

        .nav-dropdown-btn:hover {
            color: #0f172a !important; /* slate-900 */
            background-color: #f8fafb !important;
        }

        .dropdown-toggle {
            display: flex !important;
            align-items: center !important;
            gap: 4px !important;
            color: #4b5563 !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            padding: 8px 12px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
            background: transparent !important;
            border: none !important;
            font-family: 'Raleway', sans-serif !important;
        }

        .dropdown-toggle:hover {
            color: #1f2937 !important;
            background-color: #f9fafb !important;
        }

        /* Ensure dropdown menus are always visible */
        .q-btn-dropdown {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        /* Active navigation states */
        /* Top-level link styles */
        .top-nav-link {
            color: #334155 !important;
            font-weight: 600 !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            text-decoration: none !important;
            transition: color .2s ease, background .2s ease !important;
        }

        .top-nav-link:hover {
            color: #0f172a !important;
            background: #f8fafb !important;
        }

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

        .dropdown-active {
            color: #0055B8 !important;
            font-weight: 600 !important;
        }

        .dropdown-active .dropdown-icon {
            color: #0055B8 !important;
        }

        /* Active dropdown content item */
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
    add_global_styles()
    with ui.element('header').classes('fixed top-0 left-0 right-0 z-50 w-full h-16 px-4 shadow-md border-b').style('background-color: rgba(255, 255, 255, 0.95) !important; backdrop-filter: blur(8px) !important; border-bottom: 1px solid #e5e7eb !important; height: 64px !important; display: flex !important; align-items: center !important; justify-content: space-between !important;'):
        
        # Left: Logo section (clickable -> Home)
        with ui.row().classes('items-center gap-3 cursor-pointer').on('click', lambda: ui.navigate.to('/')):
            ui.icon('hub', size='2rem').style('color: #0055B8 !important;')
            ui.label('Dompell').classes('text-xl font-semibold').style('color: #1A1A1A !important; font-family: "Raleway", sans-serif;')
        
        # Center: Hover dropdown navigation menus 
        with ui.row().classes('flex items-center gap-4').style('position: absolute; left: 50%; transform: translateX(-50%);'):
            pass
        
        # Static links and buttons
        with ui.row().classes('flex items-center gap-4'):
            # Determine active states for static links
            home_active = current_page == '/'
            about_active = current_page == '/about'
            jobs_active = current_page.startswith('/jobs')
            how_active = current_page.startswith('/how-it-works')
            contact_active = current_page.startswith('/contact')
            # Resources should not be active on standalone top links like About or How
            resources_active = (current_page.startswith('/help-and-support') or current_page.startswith('/resources'))

            home_classes = 'nav-active' if home_active else ''
            about_classes = 'nav-active' if about_active else ''
            jobs_classes = 'nav-active' if jobs_active else ''
            how_classes = 'nav-active' if how_active else ''
            contact_classes = 'nav-active' if contact_active else ''

            ui.link('Home', '/').classes(f'top-nav-link {home_classes}')
            ui.link('About Us', '/about').classes(f'top-nav-link {about_classes}')
            ui.link('How it works', '/how-it-works').classes(f'top-nav-link {how_classes}')

            # Resources hover dropdown
            resources_classes = 'dropdown-hover dropdown-active' if resources_active else 'dropdown-hover'
            with ui.element('div').classes(resources_classes).style('padding: 8px 16px;'):
                label_style = 'font-family: "Raleway", sans-serif; font-weight: 600; color: #0055B8;' if resources_active else 'font-family: "Raleway", sans-serif; font-weight: 500; color: #4b5563;'
                icon_style = 'color: #0055B8; font-size: 20px;' if resources_active else 'color: #4b5563; font-size: 20px;'

                with ui.row().classes('items-center gap-1 cursor-pointer'):
                    ui.label('Resources').style(label_style)
                    ui.icon('arrow_drop_down').classes('dropdown-icon').style(icon_style)
                
                with ui.element('div').classes('dropdown-content'):
                    resource_links = [
                        {'name': 'Contact Us', 'path': '/contact'},
                        {'name': 'Trainings/Bootcamps', 'path': '/training-program-directory'},
                        {'name': 'Success Stories', 'path': '/candidates/success-stories'},
                        {'name': 'Help & Support', 'path': '/help-and-support'},
                    ]
                    ui.html(
                        f'''
                        <div class="flex flex-col p-2">
                            {(''.join(f'<a href="{link["path"]}" class="nav-dropdown-btn {"active" if current_page == link["path"] else ""}">{link["name"]}</a>' for link in resource_links))}
                        </div>
                        ''', sanitize=lambda s: s)

            # Contact link removed (now available under Resources dropdown)

            # about_classes = 'nav-active' if about_active else ''
            # ui.link('About', '/about').classes(about_classes).style('text-decoration: none;')

            # Conditional buttons based on authentication state
            if not is_authenticated():
                ui.button('Login', on_click=lambda: ui.navigate.to('/login')).classes('bg-white border').style('color: #0055B8 !important; border-color: #0055B8 !important;')
                ui.button('Register', on_click=lambda: ui.navigate.to('/login?tab=Sign+Up')).classes('bg-blue-600 text-white')
            else:
                # Show dashboard and profile links for authenticated users
                user = get_current_user()
                user_name = user.get('name', user.get('email', 'User')) if user else 'User'
                user_role = user.get('role', 'USER') if user else 'USER'
                
                with ui.row().classes('items-center gap-4'):
                    ui.icon('notifications', size='1.5rem').classes('cursor-pointer text-gray-600 hover:text-blue-600')
                    
                    with ui.menu() as menu:
                        # Role-based menu items (avoid generic duplicate 'Dashboard')

                        if user_role == 'ADMIN':
                            ui.menu_item('Admin Dashboard', on_click=lambda: ui.navigate.to('/admin/dashboard'))
                        elif user_role == 'TRAINEE':
                            ui.menu_item('My Dashboard', on_click=lambda: ui.navigate.to('/candidates/dashboard'))
                        elif user_role == 'EMPLOYER':
                            ui.menu_item('Employer Dashboard', on_click=lambda: ui.navigate.to('/employers/dashboard'))
                            ui.menu_item('Job Postings', on_click=lambda: ui.navigate.to('/employer/job-posting'))
                        
                        # Common menu items for all authenticated users
                        ui.menu_item('Profile Settings', on_click=lambda: ui.navigate.to('/settings/profile'))
                        ui.separator()
                        ui.menu_item(f'Logout ({user_name})', on_click=logout)

                    # Show user profile image or initials
                    # Try to get profile picture from user data
                    profile_pic_url = ''
                    if user:
                        # Check if user has traineeProfile with profilePictureUrl
                        trainee_profile = user.get('traineeProfile', {})
                        profile_pic_url = trainee_profile.get('profilePictureUrl', '') if trainee_profile else ''
                    
                    if profile_pic_url and profile_pic_url.strip():
                        # Show profile image
                        with ui.element('div').style('width: 36px; height: 36px; border-radius: 50%; overflow: hidden; border: 2px solid #0055B8; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.15);').on('click', menu.open):
                            ui.image(profile_pic_url).style('width: 100%; height: 100%; object-fit: cover; object-position: center;')
                    else:
                        # Show initials in a circle
                        initials = ''.join([n[0].upper() for n in user_name.split()[:2]])
                        with ui.element('div').style('width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #0055B8 0%, #0066CC 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 14px; cursor: pointer; box-shadow: 0 2px 6px rgba(0,85,184,0.3);').on('click', menu.open):
                            ui.label(initials)
