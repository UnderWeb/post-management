// src/features/posts/postsThunks.ts
import { createAsyncThunk } from '@reduxjs/toolkit';
import apiClient from '../../api/axios';
import type {
  CreatePostRequest,
  Post,
} from '../../types/post';


export const fetchPosts = createAsyncThunk(
  'posts/fetchPosts',
  async () => {
    const response = await apiClient.get<Post[]>(
      '/api/posts',
    );

    return response.data;
  },
);


export const createPost = createAsyncThunk(
  'posts/createPost',
  async (payload: CreatePostRequest) => {
    const response = await apiClient.post<Post>(
      '/api/posts',
      payload,
    );

    return response.data;
  },
);


export const deletePost = createAsyncThunk(
  'posts/deletePost',
  async (id: number) => {
    await apiClient.delete(
      `/api/posts/${id}`,
    );

    return id;
  },
);
