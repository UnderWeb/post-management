// src/features/posts/postsSlice.ts
import {
  createSlice,
} from '@reduxjs/toolkit';
import {
  fetchPosts,
  createNewPost,
  removePost,
} from './postsThunks';
import type {
  Post,
} from '../../types/post';

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

  extraReducers(builder) {
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
          action.error.message ?? 'Error loading posts';
      })
      .addCase(createNewPost.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      .addCase(removePost.fulfilled, (state, action) => {
        state.items =
          state.items.filter(
            (post) => post.id !== action.payload,
          );
      });
  },
});


export default postsSlice.reducer;
