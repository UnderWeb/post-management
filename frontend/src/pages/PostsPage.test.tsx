// src/pages/PostsPage.test.tsx
import {
  describe,
  expect,
  it,
  vi,
} from 'vitest';
import {
  render,
  screen,
} from '@testing-library/react';
import PostsPage from './PostsPage';

vi.mock(
  '../hooks',
  () => ({
    useAppDispatch: () => vi.fn(),

    useAppSelector: vi.fn(
      (selector) =>
        selector({
          posts: {
            items: [],
            loading: false,
            error: null,
          },
        }),
    ),
  }),
);

describe('PostsPage', () => {
  it('renders page title', () => {
    render(
      <PostsPage />,
    );

    expect(
      screen.getByText('Posts'),
    ).toBeInTheDocument();
  });

  it('renders loading state', async () => {
    const hooks =
      await import('../hooks');

    vi.mocked(
      hooks.useAppSelector,
    ).mockImplementation(
      (selector) =>
        selector({
          posts: {
            items: [],
            loading: true,
            error: null,
          },
        }),
    );

    render(
      <PostsPage />,
    );

    expect(
      screen.getByText(/cargando posts/i)
    ).toBeInTheDocument();

  });
});
