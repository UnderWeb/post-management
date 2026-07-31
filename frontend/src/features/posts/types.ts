// src/features/posts/types.ts
export interface Post {
  id: number;
  nombre: string;
  descripcion: string;
  resumen: Record<string, unknown>;
  fecha_creacion: string;
}
