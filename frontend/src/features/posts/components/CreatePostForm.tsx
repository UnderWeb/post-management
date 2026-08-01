// frontend/src/features/posts/components/CreatePostForm.tsx
/**
 * Form component for creating a new post with optional file upload.
 */
import { useState } from 'react';
import { useAppDispatch } from '../../../hooks';
import { createNewPost } from '../postsThunks';

function CreatePostForm() {
  const dispatch = useAppDispatch();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);

  function handleSubmit(event: React.SyntheticEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || !description.trim()) {
      return;
    }

    const formData = new FormData();
    formData.append('title', title.trim());
    formData.append('description', description.trim());
    if (file) {
      formData.append('file', file);
    }

    dispatch(createNewPost(formData));

    setTitle('');
    setDescription('');
    setFile(null);
    
    // Reset file input visually
    const fileInput = document.getElementById('file-input') as HTMLInputElement | null;
    if (fileInput) fileInput.value = '';
  }

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  }

  return (
    <form className="create-post-form" onSubmit={handleSubmit}>
      <input
        className="form-input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Título"
        required
      />
      <input
        className="form-input"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Descripción"
        required
      />
      <input
        id="file-input"
        className="form-input"
        type="file"
        onChange={handleFileChange}
      />
      <button className="primary-button" type="submit">
        Crear
      </button>
    </form>
  );
}

export default CreatePostForm;
