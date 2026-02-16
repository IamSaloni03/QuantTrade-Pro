export const formatCurrency = (value) => {
  if (value === null || value === undefined) return "₹ 0";

  return `₹ ${Number(value).toLocaleString(undefined, {
    maximumFractionDigits: 2
  })}`;
};
