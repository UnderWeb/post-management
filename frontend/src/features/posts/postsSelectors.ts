// src/features/posts/postsSelectors.ts
import type { RootState } from '../../app/store';


export const selectPosts = (
  state: RootState,
) => state.posts.items;


export const selectPostsLoading = (
  state: RootState,
) => state.posts.loading;


export const selectPostsError = (
  state: RootState,
) => state.posts.error;
