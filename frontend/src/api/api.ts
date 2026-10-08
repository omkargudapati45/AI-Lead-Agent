import axios from "axios";
import type { Lead, LeadCreate, LeadHistory } from "../types";

const API_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
});

export const getLeads = async (): Promise<Lead[]> => {
  const response = await api.get("/leads/");
  return response.data;
};

export const getLead = async (id: number): Promise<Lead> => {
  const response = await api.get(`/leads/${id}`);
  return response.data;
};

export const createLead = async (lead: LeadCreate): Promise<Lead> => {
  const response = await api.post("/leads/", lead);
  return response.data;
};

export const updateLeadStatus = async (id: number, status: string): Promise<Lead> => {
  const response = await api.put(`/leads/${id}`, { status });
  return response.data;
};

export const getLeadHistory = async (id: number): Promise<LeadHistory[]> => {
  const response = await api.get(`/leads/${id}/history`);
  return response.data;
};
