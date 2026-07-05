import request from './client';

export const getAnalytics = () => request('/api/analytics');

export const getHealth = () => request('/health');

export const computeWer = (reference, hypothesis) =>
  request('/api/evaluation/wer', {
    method: 'POST',
    body: JSON.stringify({ reference, hypothesis }),
  });
