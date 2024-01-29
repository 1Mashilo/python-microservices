import React, { PropsWithRef,SyntheticEvent, useEffect, useState } from 'react';
import {  useNavigate, useParams } from 'react-router-dom';
import { Product } from '../interfaces/products';

const ProductsEdit = (props: PropsWithRef<any>) => {
    const [title, setTitle] = useState('');
    const [image, setImage]= useState('');
    const [redirect, setRedirect]= useState(false);
    let navigate = useNavigate()
    const {id} =useParams();

    
    useEffect(() => {
        (
            
            async () => {
                const response = await fetch(`http://localhost:8000/api/products/${id}`);

                const product: Product = await response.json();

                setTitle(product.title);
                setImage(product.image)
            }
        )();
    }, []);

    const submit = async(e: SyntheticEvent)=>{
        e.preventDefault();
        
        await fetch(`http://localhost:8000/api/products/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                title,
                image
            })
        });

        setRedirect(true);

    }

    if(redirect){
        navigate('/admin/products');
    }
    
  return (
      <div className='col-md-9 ms-sm-auto col-lg-10 px-md-4'>
          <form onSubmit={submit}>
              <div className="form-group">
                  <label>Title</label>
                  <input type="text" className="form-control" name="title"
                         defaultValue={title} onChange={e=> setTitle(e.target.value)}/>
              </div>
              <div className="form-group">
                  <label>Image</label>
                  <input type="text" className="form-control" name="image"
                      defaultValue={image}  onChange={e=> setImage(e.target.value)} />
              </div>
              <button className='btn btn-outline-secondary'>Save</button>
          </form>
      </div>
  );
};

export default ProductsEdit;