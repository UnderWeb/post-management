// frontend/src/features/posts/postsThunks.test.ts
import { describe, expect, it, vi } from 'vitest';
import { getPosts, createPost, deletePost } from '../../api/postsApi';
import { fetchPosts, createNewPost, removePost } from './postsThunks';

vi.mock('../../api/postsApi', () => ({
  getPosts: vi.fn(),
  createPost: vi.fn(),
  deletePost: vi.fn(),
}));

const post = {
  id: 1,
  title: 'Post test',
  description: 'Descripción test',
  summary: { summary: 'Resumen', keywords: ['test'] },
  file_path: null,
  created_at: '2026-07-31T00:00:00',
};

describe('postsThunks', () => {
  it('fetchPosts should return posts', async () => {
    vi.mocked(getPosts).mockResolvedValue([post]);
    const dispatch = vi.fn();
    const getState = vi.fn();

    const result = await fetchPosts()(dispatch, getState, undefined);

    expect(result.type).toBe('posts/fetchPosts/fulfilled');
    expect(result.payload).toEqual([post]);
    expect(getPosts).toHaveBeenCalledTimes(1);
  });

  it('createNewPost should create a post', async () => {
    vi.mocked(createPost).mockResolvedValue(post);
    const dispatch = vi.fn();
    const getState = vi.fn();
    const formData = new FormData();
    formData.append('title', 'Post test');
    formData.append('description', 'Descripción test');

    const result = await createNewPost(formData)(dispatch, getState, undefined);

    expect(result.type).toBe('posts/createNewPost/fulfilled');
    expect(result.payload).toEqual(post);
    expect(createPost).toHaveBeenCalledWith(formData);
  });

  it('removePost should delete a post', async () => {
    vi.mocked(deletePost).mockResolvedValue();
    const dispatch = vi.fn();
    const getState = vi.fn();

    const result = await removePost(post.id)(dispatch, getState, undefined);

    expect(result.type).toBe('posts/removePost/fulfilled');
    expect(result.payload).toBe(post.id);
    expect(deletePost).toHaveBeenCalledWith(post.id);
  });
});
