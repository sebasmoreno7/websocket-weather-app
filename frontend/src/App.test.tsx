import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('shows the weather sign-in screen', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /weather monitor/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /continuar con google/i })).toBeInTheDocument();
});
