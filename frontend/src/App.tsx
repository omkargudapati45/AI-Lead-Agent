import React, { useEffect, useState } from "react";
import { getLeads, createLead, updateLeadStatus } from "./api/api";
import type { Lead } from "./types";
import { Activity, Mail, AlertCircle, Plus, X, Check, XCircle } from "lucide-react";

function App() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  const fetchLeads = async () => {
    try {
      const data = await getLeads();
      setLeads(data);
    } catch (error) {
      console.error("Failed to fetch leads", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
    const interval = setInterval(fetchLeads, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleSimulateLead = async () => {
    try {
      await createLead({
        name: "Test User " + Math.floor(Math.random() * 100),
        email: "test@example.com",
        company: "Acme Corp",
        source: "Website",
        message: "We are opening a new office and need 50 laptops and 20 monitors as soon as possible. Please send a quote.",
      });
      fetchLeads();
    } catch (error) {
      console.error("Failed to create lead", error);
    }
  };

  const handleAction = async (id: number, status: string) => {
    try {
      await updateLeadStatus(id, status);
      setSelectedLead(null);
      fetchLeads();
    } catch (error) {
      console.error("Failed to update status", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Lead Agent Dashboard</h1>
            <p className="text-gray-500 mt-1">Intelligent Lead Management & Human-in-the-Loop Workflow</p>
          </div>
          <button 
            onClick={handleSimulateLead}
            className="flex items-center gap-2 bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition shadow-sm"
          >
            <Plus size={20} /> Simulate Inbound Lead
          </button>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-3 bg-blue-100 text-blue-600 rounded-lg"><Activity size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Total Leads</p>
              <p className="text-2xl font-bold">{leads.length}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-3 bg-green-100 text-green-600 rounded-lg"><Mail size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">New / Action Required</p>
              <p className="text-2xl font-bold">{leads.filter(l => l.status === 'NEW').length}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-3 bg-red-100 text-red-600 rounded-lg"><AlertCircle size={24} /></div>
            <div>
              <p className="text-sm text-gray-500 font-medium">High Priority Leads</p>
              <p className="text-2xl font-bold">{leads.filter(l => l.priority === 'HIGH').length}</p>
            </div>
          </div>
        </div>

        {/* Lead Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">Recent Leads</h2>
          </div>
          {loading ? (
            <p className="p-6 text-gray-500">Loading leads...</p>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 text-gray-600 text-sm border-b border-gray-100">
                  <th className="p-4 font-medium">Name/Company</th>
                  <th className="p-4 font-medium">AI Intent</th>
                  <th className="p-4 font-medium">AI Priority</th>
                  <th className="p-4 font-medium">Status</th>
                  <th className="p-4 font-medium">Action</th>
                </tr>
              </thead>
              <tbody>
                {leads.map(lead => (
                  <tr key={lead.id} className="border-b border-gray-50 hover:bg-gray-50 transition cursor-pointer" onClick={() => setSelectedLead(lead)}>
                    <td className="p-4">
                      <p className="font-medium text-gray-900">{lead.name}</p>
                      <p className="text-sm text-gray-500">{lead.company}</p>
                    </td>
                    <td className="p-4">
                      <span className="text-sm font-medium text-gray-700 bg-gray-100 px-2 py-1 rounded">
                        {lead.intent || "Processing..."}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                        lead.priority === 'HIGH' ? 'bg-red-100 text-red-700' :
                        lead.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                        lead.priority === 'LOW' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                      }`}>
                        {lead.priority}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                        lead.status === 'CONVERTED' ? 'bg-green-100 text-green-700' :
                        lead.status === 'DISCARDED' ? 'bg-gray-100 text-gray-500' : 'bg-blue-100 text-blue-700'
                      }`}>
                        {lead.status}
                      </span>
                    </td>
                    <td className="p-4">
                      <button 
                        className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                        onClick={(e) => { e.stopPropagation(); setSelectedLead(lead); }}
                      >
                        Review AI Draft &rarr;
                      </button>
                    </td>
                  </tr>
                ))}
                {leads.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-8 text-center text-gray-500">
                      No leads yet. Click "Simulate Inbound Lead" to test the AI workflow!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Human-in-the-Loop Modal */}
      {selectedLead && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
            
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h2 className="text-xl font-bold text-gray-900">Lead Review: {selectedLead.name}</h2>
              <button onClick={() => setSelectedLead(null)} className="text-gray-400 hover:text-gray-700 transition">
                <X size={24} />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto flex-1 space-y-6">
              
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Original Message</h3>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-100 text-gray-700 italic">
                  "{selectedLead.message}"
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                  <h3 className="text-sm font-semibold text-blue-800 mb-1">AI Extracted Intent</h3>
                  <p className="text-blue-900 font-medium">{selectedLead.intent || "N/A"}</p>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg border border-purple-100">
                  <h3 className="text-sm font-semibold text-purple-800 mb-1">Requirements Summary</h3>
                  <p className="text-purple-900 font-medium">{selectedLead.requirement_summary || "N/A"}</p>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">AI Drafted Email Response</h3>
                <div className="bg-white p-4 rounded-lg border border-gray-200 text-gray-800 whitespace-pre-wrap font-serif">
                  {selectedLead.draft_response || "Waiting for AI to generate..."}
                </div>
              </div>
              
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Recommended Sales Action</h3>
                <div className="bg-yellow-50 p-3 rounded-lg border border-yellow-200 text-yellow-800 font-medium flex items-center gap-2">
                  <AlertCircle size={18} />
                  {selectedLead.recommended_action || "Waiting for AI..."}
                </div>
              </div>

            </div>

            {/* Modal Footer (Human Actions) */}
            <div className="p-6 border-t border-gray-100 bg-gray-50 flex justify-end gap-3">
              <button 
                onClick={() => handleAction(selectedLead.id, 'DISCARDED')}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition font-medium"
              >
                <XCircle size={18} /> Discard Lead
              </button>
              <button 
                onClick={() => handleAction(selectedLead.id, 'CONVERTED')}
                className="flex items-center gap-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium shadow-sm"
              >
                <Check size={18} /> Approve & Send Email
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}

export default App;
