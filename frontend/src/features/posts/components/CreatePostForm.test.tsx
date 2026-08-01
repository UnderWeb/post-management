// frontend/src/features/posts/components/CreatePostForm.test.tsx
/**
 * Tests for the CreatePostForm component.
 */
import { describe, expect, it, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import CreatePostForm from './CreatePostForm';

const dispatch = vi.fn();

vi.mock('../../../hooks', () => ({
  useAppDispatch: () => dispatch,
}));

describe('CreatePostForm', () => {
  it('does not submit empty form', () => {
    render(<CreatePostForm />);

    fireEvent.click(
      screen.getByRole('button', { name: /crear/i }),
    );

    expect(dispatch).not.toHaveBeenCalled();
  });

  it('creates a post with FormData', () => {
    render(<CreatePostForm />);

    fireEvent.change(screen.getByPlaceholderText('Título'), {
      target: { value: 'Nuevo' },
    });

    fireEvent.change(screen.getByPlaceholderText('Descripción'), {
      target: { value: 'Descripción nueva' },
    });

    fireEvent.click(
      screen.getByRole('button', { name: /crear/i }),
    );

    expect(dispatch).toHaveBeenCalledTimes(1);
    
    // Verify dispatch was called with a function (the thunk)
    const dispatchedThunk = dispatch.mock.calls[0][0];
    expect(typeof dispatchedThunk).toBe('function');
  });
});
