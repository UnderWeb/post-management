// src/types/post.ts
export interface Post {
  id: number;
  nombre: string;
  descripcion: string;
  resumen: {
    summary: string;
    keywords: string[];
  };
  fecha_creacion: string;
}

export interface CreatePostRequest {
  nombre: string;
  descripcion: string;
}
