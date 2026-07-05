import request from './client';

export const uploadVisit = (formData) =>
  request('/api/uploads', { method: 'POST', body: formData });

export const transcribeVisit = (visitId) =>
  request(`/api/visits/${visitId}/transcribe`, { method: 'POST' });

export const extractEntities = (visitId) =>
  request(`/api/visits/${visitId}/entities`, { method: 'POST' });

export const generateSoap = (visitId) =>
  request(`/api/visits/${visitId}/soap`, { method: 'POST' });

export const updateSoap = (visitId, soap) =>
  request(`/api/visits/${visitId}/soap`, {
    method: 'PATCH',
    body: JSON.stringify(soap),
  });

export const updateStatus = (visitId, status) =>
  request(`/api/visits/${visitId}/status`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  });

export const getVisits = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return request(`/api/visits${query ? `?${query}` : ''}`);
};

export const getVisit = (visitId) => request(`/api/visits/${visitId}`);

export const processVisit = async (visitId) => {
  await transcribeVisit(visitId);
  await extractEntities(visitId);
  return generateSoap(visitId);
};
