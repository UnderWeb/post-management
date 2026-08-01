// frontend/src/features/posts/postsThunks.ts
/**
 * Redux thunks for asynchronous post operations.
 */
import { createAsyncThunk } from '@reduxjs/toolkit';
import { getPosts, createPost, deletePost } from '../../api/postsApi';

export const fetchPosts = createAsyncThunk('posts/fetchPosts', async () => {
  return await getPosts();
});

export const createNewPost = createAsyncThunk(
  'posts/createNewPost',
  async (formData: FormData) => {
    return await createPost(formData);
  }
);

export const removePost = createAsyncThunk(
  'posts/removePost',
  async (id: number) => {
    await deletePost(id);
    return id;
  }
);
