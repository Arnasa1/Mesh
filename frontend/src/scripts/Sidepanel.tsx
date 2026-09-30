import React from 'react';
 
type MenuItem = {
    label: string;
    path: string;
};
 
const SidebarMenu: React.FC<{ menuItems: MenuItem[] }> = ({ menuItems }) => {
    return (
        <nav className="sidebar-menu">
            <ul>
                {menuItems.map((item, index) => (
                    <li key={index}>
                        <a href={item.path}>{item.label}</a>
                    </li>
                ))}
            </ul>
        </nav>
    );
};
 
export default SidebarMenu;