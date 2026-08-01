// frontend/src/features/posts/components/PostCard.test.tsx
/**
 * Tests for the PostCard component.
 */
import { describe, expect, it, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import PostCard from './PostCard';
import type { Post } from '../../../types/post';

const dispatch = vi.fn();

vi.mock('../../../hooks', () => ({
  useAppDispatch: () => dispatch,
}));

const post: Post = {
  id: 1,
  title: 'Post ejemplo',
  description: 'Descripción ejemplo',
  summary: {
    summary: 'Resumen',
    keywords: ['test'],
  },
  file_path: null,
  created_at: '2026-07-31T00:00:00',
};

describe('PostCard', () => {
  it('renders post data', () => {
    render(<PostCard post={post} />);

    expect(screen.getByText('Post ejemplo')).toBeInTheDocument();
    expect(screen.getByText('Descripción ejemplo')).toBeInTheDocument();
  });

  it('dispatches delete action', () => {
    render(<PostCard post={post} />);

    fireEvent.click(
      screen.getByRole('button', {
        name: /eliminar/i,
      }),
    );

    expect(dispatch).toHaveBeenCalledTimes(1);
  });
});
