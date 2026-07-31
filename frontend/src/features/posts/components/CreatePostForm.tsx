// src/features/posts/components/CreatePostForm.tsx
import {
  useState,
} from 'react';

import type {
  SyntheticEvent,
} from 'react';

import {
  useAppDispatch,
} from '../../../hooks';

import {
  createNewPost,
} from '../postsThunks';


function CreatePostForm() {
  const dispatch = useAppDispatch();

  const [
    nombre,
    setNombre,
  ] = useState('');

  const [
    descripcion,
    setDescripcion,
  ] = useState('');


  function handleSubmit(
    event: SyntheticEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!nombre.trim() || !descripcion.trim()) {
      return;
    }

    dispatch(
      createNewPost({
        nombre: nombre.trim(),
        descripcion: descripcion.trim(),
      }),
    );

    setNombre('');
    setDescripcion('');
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={nombre}
        onChange={(event) =>
          setNombre(event.target.value)
        }
        placeholder='Nombre'
      />
      <textarea
        value={descripcion}
        onChange={(event) =>
          setDescripcion(event.target.value)
        }
        placeholder='Descripción'
      />
      <button type='submit'>
        Crear
      </button>
    </form>
  );
}

export default CreatePostForm;
