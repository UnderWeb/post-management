// src/features/posts/postsSlice.ts
import { createSlice } from '@reduxjs/toolkit';
import type { Post } from '../../types/post';
import {
  createPost,
  deletePost,
  fetchPosts,
} from './postsThunks';

interface PostsState {
  items: Post[];
  loading: boolean;
  error: string | null;
}

const initialState: PostsState = {
  items: [],
  loading: false,
  error: null,
};

const postsSlice = createSlice({
  name: 'posts',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder

      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })

      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error =
          action.error.message ?? 'Unexpected error';
      })

      .addCase(createPost.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })

      .addCase(deletePost.fulfilled, (state, action) => {
        state.items = state.items.filter(
          (post) => post.id !== action.payload,
        );
      });
  },
});

export default postsSlice.reducer;
