import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

const originalClientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;

afterEach(() => {
  if (originalClientId === undefined) {
    delete process.env.REACT_APP_GOOGLE_CLIENT_ID;
  } else {
    process.env.REACT_APP_GOOGLE_CLIENT_ID = originalClientId;
  }
});

test('explains when Google sign-in is not configured', () => {
  delete process.env.REACT_APP_GOOGLE_CLIENT_ID;
  render(<App />);
  expect(screen.getByRole('heading', { name: /weather monitor/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /continuar con google/i })).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /continuar con google/i })).toBeDisabled();
  expect(screen.getByRole('alert')).toHaveTextContent(/no está configurado/i);
});

test('enables Google sign-in when a client ID is configured', () => {
  process.env.REACT_APP_GOOGLE_CLIENT_ID = 'test-client-id';
  render(<App />);
  expect(screen.getByRole('button', { name: /continuar con google/i })).toBeEnabled();
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});
