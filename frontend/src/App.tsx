import './App.css';
import Products from './admin/Products';
import Main from './main/Main';
import ProductsCreate from './admin/ProductsCreate';
import ProductsEdit from './admin/ProductsEdit';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <main role="main" className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/admin/products" element={<Products />} />
            <Route path="/admin/products/create" element={<ProductsCreate />} />
            <Route path="/admin/products/:id/edit" element={<ProductsEdit />} />
          </Routes>
        </BrowserRouter>
      </main>
    </div>
  );
}

export default App;
