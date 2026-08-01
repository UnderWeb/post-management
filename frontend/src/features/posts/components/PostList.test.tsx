// frontend/src/features/posts/components/PostList.test.tsx
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import PostList from './PostList';
import postsReducer from '../postsSlice';
import type { Post } from '../../../types/post';

const posts: Post[] = [
  {
    id: 1,
    title: 'Post 1',
    description: 'Descripción 1',
    summary: {
      summary: 'Resumen 1',
      keywords: ['test'],
    },
    file_path: null,
    created_at: '2026-07-31T00:00:00',
  },
  {
    id: 2,
    title: 'Post 2',
    description: 'Descripción 2',
    summary: {
      summary: 'Resumen 2',
      keywords: ['test'],
    },
    file_path: null,
    created_at: '2026-07-31T00:00:00',
  },
];

function renderWithStore(component: React.ReactNode) {
  const store = configureStore({
    reducer: {
      posts: postsReducer,
    },
  });

  return render(
    <Provider store={store}>
      {component}
    </Provider>,
  );
}

describe('PostList', () => {
  it('renders posts', () => {
    renderWithStore(<PostList posts={posts} />);

    expect(screen.getByText('Post 1')).toBeInTheDocument();
    expect(screen.getByText('Post 2')).toBeInTheDocument();
  });

  it('renders empty table when no posts exist', () => {
    const { container } = renderWithStore(<PostList posts={[]} />);

    // Verify the table exists but has no rows in tbody
    const table = container.querySelector('table');
    expect(table).toBeInTheDocument();

    const tbody = container.querySelector('tbody');
    expect(tbody).toBeInTheDocument();
    expect(tbody?.children.length).toBe(0);

    expect(screen.queryByText('Post 1')).not.toBeInTheDocument();
  });
});
