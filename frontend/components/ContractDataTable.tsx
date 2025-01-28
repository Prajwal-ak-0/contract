import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Pen } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import axios from "axios";
import { toast } from "sonner";

interface Field {
  name: string;
  value: string;
  page: number;
}

interface ContractDataTableProps {
  fields: Field[];
  docType: string;
  handleEditField: (field: Field) => void;
  handleSaveEdit: (name: string, newValue: string, newPage: string) => void;
  editingField: Field | null;
  setEditingField: React.Dispatch<React.SetStateAction<Field | null>>;
  isDialogOpen: boolean;
  setIsDialogOpen: React.Dispatch<React.SetStateAction<boolean>>;
  closeDialogRef: React.RefObject<HTMLButtonElement>;
  onFieldClick: (page: number) => void;
  fieldConfidence?: Record<string, number>;
  fieldReasoning?: Record<string, string>;
}

const getConfidenceBadgeColor = (confidence: number) => {
  if (confidence >= 8) return "bg-green-500 hover:bg-green-600";
  if (confidence >= 5) return "bg-yellow-500 hover:bg-yellow-600";
  return "bg-red-500 hover:bg-red-600";
};

const ContractDataTable: React.FC<ContractDataTableProps> = ({
  fields,
  docType,
  handleEditField,
  handleSaveEdit,
  editingField,
  setEditingField,
  isDialogOpen,
  setIsDialogOpen,
  closeDialogRef,
  onFieldClick,
  fieldConfidence,
  fieldReasoning,
}) => {
  const [editValue, setEditValue] = React.useState("");
  const [editPage, setEditPage] = React.useState("");

  React.useEffect(() => {
    if (editingField) {
      setEditValue(editingField.value);
      setEditPage(editingField.page.toString());
    }
  }, [editingField]);

  const handleSave = async () => {
    try {
      const response = await axios.post("/api/update-field", {
        doc_type: docType.toUpperCase(),
        field_name: editingField?.name,
        updated_value: editValue,
      });

      handleSaveEdit(editingField?.name || "", editValue, editPage);
      setIsDialogOpen(false);
      toast.success("Value updated successfully");
    } catch (error: any) {
      toast.error(error.message || "Failed to update value");
    }
  };

  return (
    <div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Field Name</TableHead>
            <TableHead>Value</TableHead>
            <TableHead>Page</TableHead>
            <TableHead>Confidence</TableHead>
            <TableHead>Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {fields.map((field) => (
            <TableRow
              key={field.name}
              className="cursor-pointer relative group transition-colors duration-200 hover:bg-blue-50 dark:hover:bg-blue-900/20"
              onClick={() => field.page > 0 && onFieldClick(field.page)}
            >
              <TableCell className="font-medium">
                {field.name}
                <HoverCard openDelay={1000}>
                  <HoverCardTrigger asChild>
                    <div className="absolute inset-0 z-10" />
                  </HoverCardTrigger>
                  <HoverCardContent 
                    className="w-80 backdrop-blur-lg bg-blue-50 dark:bg-gray-800/95 p-4 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700"
                    align="start"
                    side="right"
                  >
                    <div className="space-y-2">
                      <h4 className="text-sm font-semibold text-black dark:text-white">Reasoning for {field.name}</h4>
                      <p className="text-sm text-gray-700 dark:text-gray-300">
                        {fieldReasoning?.[field.name] || "No reasoning provided"}
                      </p>
                    </div>
                  </HoverCardContent>
                </HoverCard>
              </TableCell>
              <TableCell>{field.value}</TableCell>
              <TableCell>{field.page > 0 ? field.page : "N/A"}</TableCell>
              <TableCell>
                {fieldConfidence?.[field.name] !== undefined && (
                  <Badge
                    className={`${getConfidenceBadgeColor(
                      fieldConfidence[field.name]
                    )} text-white transition-colors`}
                  >
                    {fieldConfidence[field.name]}
                  </Badge>
                )}
              </TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleEditField(field);
                  }}
                >
                  <Pen className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle className="text-black">Edit Field</DialogTitle>
          </DialogHeader>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSave();
            }}
          >
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="name" className="text-right">
                  Name
                </Label>
                <Input
                  id="name"
                  value={editingField?.name || ""}
                  className="col-span-3 text-black"
                  disabled
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="value" className="text-right">
                  Value
                </Label>
                <Input
                  id="value"
                  value={editValue}
                  className="col-span-3 text-black"
                  onChange={(e) => setEditValue(e.target.value)}
                  required
                />
              </div>
              <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="page" className="text-right">
                  Page
                </Label>
                <Input
                  id="page"
                  type="number"
                  value={editPage}
                  className="col-span-3 text-black"
                  onChange={(e) => setEditPage(e.target.value)}
                  min="1"
                  required
                  style={{ appearance: "textfield" }}
                />
              </div>
            </div>
            <DialogFooter>
              <Button type="submit">Save changes</Button>
            </DialogFooter>
          </form>
          <DialogClose className="text-black" ref={closeDialogRef} />
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ContractDataTable;
