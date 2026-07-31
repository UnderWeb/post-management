// src/api/postsApi.ts
import apiClient from './axios';
import type {
  CreatePostRequest,
  Post,
} from '../types/post';

export async function getPosts(): Promise<Post[]> {
  const response = await apiClient.get<Post[]>('/posts');

  return response.data;
}

export async function createPost(
  payload: CreatePostRequest,
): Promise<Post> {
  const response = await apiClient.post<Post>(
    '/posts',
    payload,
  );

  return response.data;
}

export async function deletePost(
  id: number,
): Promise<void> {
  await apiClient.delete(`/posts/${id}`);
}
