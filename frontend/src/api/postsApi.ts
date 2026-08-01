// frontend/src/api/postsApi.ts
/**
 * API service for Post operations.
 */
import apiClient from './axios';
import type { Post } from '../types/post';

/**
 * Fetches all posts from the API.
 */
export async function getPosts(): Promise<Post[]> {
  const response = await apiClient.get<Post[]>('/posts');
  return response.data;
}

/**
 * Creates a new post using FormData to support multipart/form-data.
 */
export async function createPost(formData: FormData): Promise<Post> {
  const response = await apiClient.post<Post>('/posts', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}

/**
 * Deletes a post by its ID.
 */
export async function deletePost(id: number): Promise<void> {
  await apiClient.delete(`/posts/${id}`);
}
