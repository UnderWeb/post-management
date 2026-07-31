// src/features/posts/postsThunks.ts
import {
  createAsyncThunk,
} from '@reduxjs/toolkit';
import {
  getPosts,
  createPost,
  deletePost,
} from '../../api/postsApi';
import type {
  CreatePostRequest,
} from '../../types/post';

export const fetchPosts =
  createAsyncThunk(
    'posts/fetch',
    async () => {
      return await getPosts();
    },
  );

export const createNewPost =
  createAsyncThunk(
    'posts/create',
    async (
      payload: CreatePostRequest,
    ) => {
      return await createPost(payload);
    },
  );

export const removePost =
  createAsyncThunk(
    'posts/delete',
    async (
      id: number,
    ) => {
      await deletePost(id);

      return id;
    },
  );
