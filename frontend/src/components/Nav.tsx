


const Nav = () => {
    return (
      <header className="navbar sticky-top bg-dark flex-md-nowrap p-0 shadow" 
      data-bs-theme="dark">
        <a className="navbar-brand col-md-3 col-lg-2 me-0 px-3 fs-6 text-white" 
        href="#">Company name</a>
        <button className="navbar-toggler position-absolute d-md-none collapsed" 
                type="button"
                data-toggle="collapse"
                data-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded='false'
                aria-label="Toggle navigation">
          <span className='navbar-toggler-icon'></span>
        </button>
        <input className="form-control w-100 rounded-0 border-0" 
              type="text" 
              placeholder="Search" 
              aria-label="Search" />
        <ul className="navbar-nav px-3">
          <li className="nav-item text-nowrap">
            <a className="nav-link" href='a'>Sign out</a>
          </li>
        </ul>
      </header>
    );
  };
  
  export default Nav;
  