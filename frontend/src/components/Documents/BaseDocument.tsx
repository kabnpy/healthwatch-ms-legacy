import { Letterhead } from "./Letterhead";

interface BaseDocumentProps {
  children: React.ReactNode;
}

export const BaseDocument = ({ children }: BaseDocumentProps) => {
  return (
    <div className="w-full h-full bg-white text-black p-12 font-sans relative">
      {/* Universal Letterhead */}
      <Letterhead />

      {/* Main Content Area */}
      <div className="min-h-[600px]">{children}</div>

      {/* Universal Footer */}
      <div className="mt-12 pt-8 border-t text-center text-[10px] text-gray-400">
        <p>
          This is a computer-generated document and is valid without a physical
          signature.
        </p>
        <p>
          HealthWatch Management System • Generated on{" "}
          {new Date().toLocaleString()}
        </p>
      </div>
    </div>
  );
};
