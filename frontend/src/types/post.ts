// src/types/post.ts
export interface PostSummary {
  summary: string;
  keywords: string[];
}

export interface Post {
  id: number;
  nombre: string;
  descripcion: string;
  resumen: PostSummary;
  fecha_creacion: string;
}

export interface CreatePostRequest {
  nombre: string;
  descripcion: string;
}
