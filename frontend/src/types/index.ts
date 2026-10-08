export type LeadStatus = "NEW" | "IN_PROGRESS" | "FOLLOW_UP_SCHEDULED" | "CONVERTED" | "DISCARDED";
export type LeadPriority = "LOW" | "MEDIUM" | "HIGH" | "UNASSIGNED";

export interface Lead {
  id: number;
  name: string | null;
  email: string | null;
  phone: string | null;
  company: string | null;
  source: string;
  message: string;
  intent: string | null;
  requirement_summary: string | null;
  status: LeadStatus;
  priority: LeadPriority;
  draft_response: string | null;
  recommended_action: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface LeadCreate {
  name?: string;
  email?: string;
  phone?: string;
  company?: string;
  source?: string;
  message: string;
}

export interface LeadHistory {
  id: number;
  lead_id: number;
  action: string;
  notes: string | null;
  created_at: string;
}
