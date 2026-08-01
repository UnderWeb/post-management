// frontend/src/types/post.ts
/**
 * Type definitions for Post entities matching the backend API.
 */

export interface Post {
  id: number;
  title: string;
  description: string;
  summary: {
    summary: string;
    keywords: string[];
  };
  file_path: string | null;
  created_at: string;
}
