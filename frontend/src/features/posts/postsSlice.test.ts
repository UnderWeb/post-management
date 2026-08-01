// frontend/src/features/posts/postsSlice.test.ts
import { describe, expect, it } from 'vitest';
import reducer from './postsSlice';
import { createNewPost, removePost } from './postsThunks';
import type { Post } from '../../types/post';

const post: Post = {
  id: 1,
  title: 'Post test',
  description: 'Descripción test',
  summary: { summary: 'Resumen', keywords: ['test'] },
  file_path: null,
  created_at: '2026-07-31T00:00:00',
};

describe('postsSlice', () => {
  it('should return initial state', () => {
    const state = reducer(undefined, { type: 'unknown' });
    expect(state.items).toEqual([]);
    expect(state.loading).toBe(false);
    expect(state.error).toBeNull();
  });

  it('should add created post', () => {
    const formData = new FormData();
    const state = reducer(undefined, createNewPost.fulfilled(post, '', formData));
    expect(state.items).toHaveLength(1);
    expect(state.items[0]).toEqual(post);
  });

  it('should remove deleted post', () => {
    const initialState = { items: [post], loading: false, error: null };
    const state = reducer(initialState, removePost.fulfilled(post.id, '', post.id));
    expect(state.items).toHaveLength(0);
  });
});
