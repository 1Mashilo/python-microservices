import Wrapper from './Wrapper';
import { Product } from '../interfaces/product';
import { useState, useEffect, SyntheticEvent } from 'react';
import { useNavigate } from 'react-router-dom';

interface ProductsEditProps {
    match: {
      params: {
        id: string;
      };
    };
  }
  
  const ProductsEdit: React.FC<ProductsEditProps> = (props)  => {
  const [title, setTitle] = useState('');
  const [image, setImage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/products/${props.match.params.id}`,
        );
        const product: Product = await response.json();
        setTitle(product.title);
        setImage(product.image);
      } catch (error) {
        console.error('Error fetching product:', error);
      }
    })();
  }, []);

  const submit = async (e: SyntheticEvent) => {
    e.preventDefault();

    try {
      await fetch(`http://localhost:8000/api/products/${props.match.params.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, image }),
      });
      navigate('/admin/products');
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };

  return (
    <Wrapper>
      <form onSubmit={submit}>
        <div className="form-group">
          <label>Title</label>
          <input
            type="text"
            className="form-control"
            name="title"
            defaultValue={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Image</label>
          <input
            type="text"
            className="form-control"
            name="image"
            defaultValue={image}
            onChange={(e) => setImage(e.target.value)}
          />
        </div>
        <button className="btn btn-outline-secondary">Save</button>
      </form>
    </Wrapper>
  );
};

export default ProductsEdit;
