export const mockResponse = {
    "extracted_data": [
      {
        "field": "client_company_name",
        "value": "Streamingo Solutions Pvt. Ltd.",
        "page_num": "1",
        "confidence": 9,
        "reasoning": "The name 'Streamingo Solutions Pvt. Ltd.' is explicitly identified as 'the customer' in the Statement of Work (SOW) on page 1 of the contract. This designation confirms it to be the client company in the context of the agreement.",
        "proof": "1 SCHEDULE 1 STATEMENT OF WORK Streamingo Solutions Pvt. Ltd. (\"the customer\") and NEXTWEALTH ENTREPRENEURS PVT. LTD. (the \"Service Provider\") enter this Statement of Work (\"SOW\") effective as on \" 31st March 2024\"."
      },
      {
        "field": "currency",
        "value": "INR",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The currency type 'Rs' is explicitly mentioned in the clauses regarding fees and payment, which indicates that the pricing is given in Indian Rupees. There are no other currency types mentioned in the text, and the context strongly suggests that 'Rs' refers to this specific currency due to the geographical context (India).",
        "proof": "NextWealth shall invoice \"Company\" as follows : FTE / Month – Rs 39,500"
      },
      {
        "field": "sow_start_date",
        "value": "2022-05-09",
        "page_num": "1",
        "confidence": 9,
        "reasoning": "The start date was extracted from the text where it explicitly states that the Master Services Agreement (MSA) is effective from '9th May 2022', indicating the commencement of the agreement.",
        "proof": "This SOW is governed by the Master Services Agreement (MSA) effective as on \"9th May 2022\"."
      },
      {
        "field": "sow_end_date",
        "value": "2024-07-31",
        "page_num": "1",
        "confidence": 9,
        "reasoning": "The contract clearly states that the project has been extended 'up until July 31st 2024' which indicates that this is the termination date for this specific project within the contract. The context around the extension shows that this date is definitive rather than approximate, thus supporting a high confidence level for the extraction.",
        "proof": "the project has now been extended from April 2024 up until July 31st 2024"
      },
      {
        "field": "cola",
        "value": "8",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The Cost of Living Adjustment (COLA) percentage was clearly stated in the contract on page 5, specifying that there will be a year-over-year increase for COLA at an exact percentage of 8%. This is straightforward and unambiguous, indicating a fixed adjustment rate.",
        "proof": "There will be a YOY increase for Cost-of-Living Adjustment (COLA) at 8% per annum."
      },
      {
        "field": "credit_period",
        "value": "30",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The credit period of 30 days is clearly stated in the contractual text, specifying that payment should be made within this timeframe after receiving the invoice. The extraction was straightforward as the term 'payment to be made within 30 days of receiving invoice' is unambiguous and specific.",
        "proof": "Invoice will be raised on the last day of the month and the payment to be made within 30 days of receiving invoice."
      },
      {
        "field": "inclusive_or_exclusive_gst",
        "value": "Exclusive",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The contract explicitly states that 'All applicable taxes (like GST) will be additional,' indicating that GST is not included in the quoted fee and will be charged separately. This corroborates that the pricing is 'Exclusive' of GST.",
        "proof": "All applicable taxes (like GST) will be additional."
      },
      {
        "field": "sow_value",
        "value": "39500",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The value was extracted from the fees and payment section of the contract, which explicitly states 'FTE / Month – Rs 39,500', indicating that this is the fixed monthly rate for the services rendered under the SOW.",
        "proof": "NextWealth shall invoice \"Company\" as follows : FTE / Month – Rs 39,500"
      },
      {
        "field": "sow_no",
        "value": "1",
        "page_num": "1",
        "confidence": 9,
        "reasoning": "The extracted SOW number '1' is explicitly mentioned in the title 'SCHEDULE 1 STATEMENT OF WORK', indicating it is the first statement of work in the document. The placement at the beginning of the contract supports it being a significant identifier for this section.",
        "proof": "1 SCHEDULE 1 STATEMENT OF WORK Streamingo Solutions Pvt. Ltd. ("
      },
      {
        "field": "type_of_billing",
        "value": "FTE Based",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The billing structure outlined mentions 'FTE / Month' which indicates that the billing is based on a fixed fee per Full-Time Equivalent (FTE) per month. This aligns with the FTE Based model.",
        "proof": "5 SCHEDULE 2 FEES AND PAYMENT NextWealth shall invoice 'Company' as follows : FTE / Month – Rs 39,500"
      },
      {
        "field": "po_number",
        "value": "null",
        "page_num": "1",
        "confidence": 2,
        "reasoning": "There is no explicit mention of a Purchase Order (PO) number in the provided contract text. The text mostly discusses the scope of work, responsibilities, and team structures but does not reference a specific PO number that fits typical formatting (like 'PO12345').",
        "proof": "The content does not contain any specific PO number; it primarily includes project details, roles, and agreements."
      },
      {
        "field": "amendment_no",
        "value": "null",
        "page_num": "1",
        "confidence": 3,
        "reasoning": "The document mentions a Master Services Agreement (MSA) with an effective date of '9th May 2022', but does not explicitly refer to an amendment number. Since no specific amendment number is provided in the text, the confidence level is low.",
        "proof": "This SOW is governed by the Master Services Agreement (MSA) effective as on \"9th May 2022\"."
      },
      {
        "field": "billing_unit_type_and_rate_cost",
        "value": "per_sample - 39500, per_item - 0",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The contract specifies a fixed monthly billing rate of Rs 39,500 for the full-time equivalent (FTE) per month. Although it does not explicitly mention per sample or per item rates separately, the closest match in terms of cost is Rs 39,500 per FTE, which applies to consistent work done typically measured in samples or items. The high confidence is due to the clear language around fees stated in Schedule 2, Page 5.",
        "proof": "NextWealth shall invoice \"Company” as follows : FTE / Month – Rs 39,500"
      },
      {
        "field": "particular_role_rate",
        "value": "FTE - 39500, Associates - 39500, Team Leads - 39500, Quality Analysts - 39500, Trainers - 39500",
        "page_num": "5",
        "confidence": 9,
        "reasoning": "The rate of Rs 39,500 is consistently applied across various roles such as Associates, Team Leads, Quality Analysts, and Trainers. It is mentioned as a fixed rate applicable for a range of positions within the scope of work, indicating clarity and certainty in pricing structure.",
        "proof": "NextWealth shall invoice \"Company” as follows : FTE / Month – Rs 39,500... The same rate is applicable for Associates as well as Team Leads, Quality Analysts and Trainers that are dedicated to this Program."
      }
    ]
  };

  // const handleFileUpload = async () => {
  //   if (file) {
  //     setIsUploading(true);
  //     try {
  //       const uploadFormData = new FormData();
  //       uploadFormData.append("file", file);
  //       uploadFormData.append("pdfType", pdfType);

  //       const response = await fetch("https://contract-backend-965571980615.us-central1.run.app/upload", {
  //         method: "POST",
  //         body: uploadFormData,
  //         credentials: "include",
  //       });

  //       if (!response.ok) {
  //         throw new Error(`HTTP error! status: ${response.status}`);
  //       }
        
  //       const result = await response.json();
  //       console.log("Response from server:", result);
        
  //       const extractedData = result.extracted_data as ExtractedDataItem[];
        
  //       // Initialize all our data objects
  //       const newApiData: ApiData = {};
  //       const newFieldPageMapping: Record<string, string> = {};
  //       const newFieldConfidence: Record<string, number> = {};
  //       const newFieldReasoning: Record<string, string> = {};

  //       // Process all data from the response
  //       extractedData.forEach(item => {
  //         // Log details for debugging
  //         console.log(`Processing field: ${item.field}`);
  //         console.log(`Value: ${item.value}`);
  //         console.log(`Page Number: ${item.page_num}`);
  //         console.log(`Confidence: ${item.confidence}`);
  //         console.log(`Reasoning: ${item.reasoning}`);
  //         console.log(`Proof: ${item.proof}`);

  //         // Store the data in our state objects
  //         newApiData[item.field] = item.value || "";
  //         newFieldPageMapping[item.field] = item.page_num;
  //         if (item.confidence !== undefined) {
  //           newFieldConfidence[item.field] = Number(item.confidence);
  //         }
  //         if (item.reasoning) {
  //           newFieldReasoning[item.field] = item.reasoning;
  //         }
  //       });

  //       // Update all our states
  //       setApiData(newApiData);
  //       setFieldPageMapping(newFieldPageMapping);
  //       setFieldConfidence(newFieldConfidence);
  //       setFieldReasoning(newFieldReasoning);

  //       // Log the processed data
  //       console.log('Processed API Data:', newApiData);
  //       console.log('Page Mapping:', newFieldPageMapping);
  //       console.log('Confidence Scores:', newFieldConfidence);
  //       console.log('Reasoning:', newFieldReasoning);

  //       // Create Excel file
  //       const allData = { ...formData, ...newApiData };
  //       const ws = XLSX.utils.json_to_sheet([allData]);
  //       const wb = XLSX.utils.book_new();
  //       XLSX.utils.book_append_sheet(wb, ws, "Contract Data");

  //       const excelBlob = new Blob(
  //         [XLSX.write(wb, { bookType: "xlsx", type: "array" })],
  //         { type: "application/octet-stream" }
  //       );
  //       setExcelFile(excelBlob);

  //       setIsDownloadReady(true);
  //       toast.success("File uploaded successfully");
  //     } catch (error) {
  //       console.error("Error uploading file:", error);
  //       if (error instanceof TypeError && error.message.includes("NetworkError")) {
  //         toast.error("Network error. Please check your connection and try again.");
  //       } else {
  //         toast.error(`An error occurred while uploading the file: ${(error as Error).message || "Unknown error"}`);
  //       }
  //     } finally {
  //       setIsUploading(false);
  //     }
  //   }
  // };


//   const handleFileUpload = async () => {
//     if (file) {
//       setIsUploading(true);
//       try {
//         console.log("Mock response:", mockResponse);
        
//         const extractedData = mockResponse.extracted_data as ExtractedDataItem[];
        
//         const newApiData: ApiData = {};
//         const newFieldPageMapping: Record<string, string> = {};

//         // Populate data from extractedData
//         extractedData.forEach((item) => {
//           newApiData[item.field] = item.value;
//           newFieldPageMapping[item.field] = item.page_num;
//           console.log(`Processing ${item.field}: ${item.value}`);
//         });

//         setApiData(newApiData);
//         console.log('newApiData', newApiData);
//         setFieldPageMapping(newFieldPageMapping);
//         console.log('newFieldPageMapping', newFieldPageMapping);

//         const allData = { ...formData, ...newApiData };
//         const ws = XLSX.utils.json_to_sheet([allData]);
//         const wb = XLSX.utils.book_new();
//         XLSX.utils.book_append_sheet(wb, ws, "Contract Data");

//         const excelBlob = new Blob(
//           [XLSX.write(wb, { bookType: "xlsx", type: "array" })],
//           { type: "application/octet-stream" }
//         );
//         setExcelFile(excelBlob);

//         setIsDownloadReady(true);
//         toast.success("File processed successfully");
//       } catch (error) {
//         console.error("Error processing file:", error);
//         toast.error(`An error occurred: ${(error as Error).message || "Unknown error"}`);
//       } finally {
//         setIsUploading(false);
//       }
//     }
//   };