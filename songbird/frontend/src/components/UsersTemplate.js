import CustomNavbarUsers from './NavbarUsers';
import SideMenu from './SideMenu';
import '../styles/App.css';

function UsersTemplate({ children }) {
  return (
    <div className='user-page'>
      <CustomNavbarUsers />
      <div className='user-page-without-header'>
        <SideMenu />
        <div className='user-content'>
          {children}
        </div>
      </div>
    </div>
  );
}

export default UsersTemplate;
